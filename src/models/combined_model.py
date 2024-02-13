import pytorch_lightning as pl
import torch as T
from torch.nn import ModuleList

class CombinedModel(pl.LightningModule):
    def __init__(self, model_1nu, model_2nu, model_3nu, model_4nu) -> None:
        super().__init__()
        self.models = ModuleList([model_1nu, model_2nu, model_3nu, model_4nu])

    def predict_step(self, batch: tuple, _batch_idx: int) -> None:
        """Single prediction step which add generates samples to the buffer."""
        misc, met, lep, jet, _ = batch
        print(lep.shape)
        print(lep[0])
        print(lep[1])
        print(lep[2])
        print(lep[3])
        print(lep[4])
        gen_nus = {}
        log_probs = {}
        for length in range(1, 5):
            print(f"length = {length}")
            lep_mask = T.any(lep != 0, dim=-1)
            mask = (lep_mask.sum(axis=1) == length)
            print(f"mask = {mask}")
            if not mask.any():
                print('continue')
                continue
            gen_nu, log_prob = self.models[length-1].sample_and_log_prob((misc[mask], met[mask], lep[mask], jet[mask]))
            print(f"gen nu shape = {gen_nu.shape}")
            print(f"log prob shape = {log_prob.shape}")
            gen_nus[f"n_neutrinos_{length}"] = gen_nu
            log_probs[f"n_neutrinos_{length}"] = log_prob
        return {"gen_nu": gen_nus, "log_prob": log_probs}
