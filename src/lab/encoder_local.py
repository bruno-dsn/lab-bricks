"""Encoder opcional em CPU; modelo e tokenizer fixados por SHA-256."""
from pathlib import Path
import hashlib
import numpy as np

REVISION='2c4055b12046f11709e9df2c122e59ffbdc2f900'
FILES={'tokenizer.json':'b60b6b43406a48bf3638526314f3d232d97058bc93472ff2de930d43686fa441',
       'model_quantized.onnx':'66fc00f5f29afcaff34092e1bdd20008ca3918265a82fb9695a551e510cc4ebc'}


class EncoderLocal:
    def __init__(self,directory):
        from tokenizers import Tokenizer
        import onnxruntime as ort
        directory=Path(directory)
        for name,sha in FILES.items():
            path=directory/name
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:
                raise ValueError('Modelo ou tokenizer não corresponde à versão registrada.')
        self.tokenizer=Tokenizer.from_file(str(directory/'tokenizer.json'))
        self.tokenizer.enable_truncation(max_length=128)
        self.tokenizer.enable_padding(pad_id=0,pad_token='<pad>')
        options=ort.SessionOptions();options.intra_op_num_threads=2;options.inter_op_num_threads=1
        self.session=ort.InferenceSession(str(directory/'model_quantized.onnx'),sess_options=options,providers=['CPUExecutionProvider'])

    def encode(self,texts):
        if not isinstance(texts,list) or not 1<=len(texts)<=2000 or not all(isinstance(t,str) and 1<=len(t)<=80_000 for t in texts):
            raise ValueError('Texto fora do orçamento do encoder.')
        outputs=[]
        for start in range(0,len(texts),16):
            encoded=self.tokenizer.encode_batch(texts[start:start+16])
            fields={'input_ids':np.array([e.ids for e in encoded],dtype=np.int64),
                    'attention_mask':np.array([e.attention_mask for e in encoded],dtype=np.int64),
                    'token_type_ids':np.array([e.type_ids for e in encoded],dtype=np.int64)}
            inputs={i.name:fields[i.name] for i in self.session.get_inputs()}
            hidden=self.session.run(None,inputs)[0]
            mask=fields['attention_mask'][...,None]
            pooled=(hidden*mask).sum(axis=1)/np.maximum(mask.sum(axis=1),1)
            pooled=pooled/np.maximum(np.linalg.norm(pooled,axis=1,keepdims=True),1e-12)
            outputs.append(pooled.astype(np.float32))
        result=np.concatenate(outputs)
        if result.shape!=(len(texts),384) or not np.isfinite(result).all():
            raise ValueError('Saída do encoder diverge do contrato.')
        return result
