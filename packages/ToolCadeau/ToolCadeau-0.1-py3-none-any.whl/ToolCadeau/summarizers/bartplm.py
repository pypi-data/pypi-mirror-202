import torch
import transformers

from nltk import sent_tokenize
from transformers import BartTokenizer, BartForConditionalGeneration
from sentence_transformers import SentenceTransformer, util

class BartSummarizer(object):

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.torch.cuda.is_available() else "cpu")
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(self.device)

        # Embedder would be used when indexing the summarized sentences.
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def summarize(self, doc, num_beams=2, length_penalty=2, no_repeat_ngram_size=4):
        """
        Args:
            doc (str): Target document
            num_beams (int): size of beam search targets in reference.
            length_penalty (float): length penalty to cover the curse of probability accumulation in language model.
            no_repeat_ngram_size (int): tolerance for repeat words in the summary.
        Func:
            Summarize the document using the pre-trained language model BART.
        """
        doc = doc.replace('\n',' ')

        doc_input_ids = self.tokenizer.batch_encode_plus(
            [doc],
            return_tensors='pt',
            truncation=True,
            max_length=1024
        )['input_ids'].to(self.device)

        summary_ids = self.model.generate(
            doc_input_ids,
            num_beams=int(num_beams),
            length_penalty=float(length_penalty),
            no_repeat_ngram_size=int(no_repeat_ngram_size)
        )

        summary_txt = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)

        # Because the summary_txt is a lot similar with original sentence in the document,
        # we can index the summary_txt using sentence_transformer.
        # The order index of the most similar sentence in the original document
        # would be mapped with the sentence in the summary_txt.
        sents = sent_tokenize(doc)
        abt_sents = sent_tokenize(summary_txt)

        embedded_sents = self.embedder.encode(sents)
        embedded_abt_sents = self.embedder.encode(abt_sents)

        dist_mat = util.cos_sim(embedded_abt_sents, embedded_sents)
        abt_indices = dist_mat.argmax(dim=-1).tolist()

        # Sometimes, bart summarization split the original sentence in several sentences, and change a little number of
        # words of the sentences to compose the summary_txt. In this case, the index of the summary_txt would be duplicated
        # because they all are originated from a single sentence.
        # At here, we are going to combine several sentences into one sentence, and give only the single index to the combined one.

        abt_itos = dict()
        for idx, sent in zip(abt_indices, abt_sents):
            if abt_itos.get(idx) is not None:
                abt_itos[idx] = " ".join([abt_itos[idx], sent])
            else:
                abt_itos[idx] = sent
        # |abt_itos| = {idx:sent, idx:sent, ...}

        return abt_itos