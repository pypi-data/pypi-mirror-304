from sklearn.base import BaseEstimator
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import numpy as np
import os
from os import PathLike
from lightning import Trainer
from lightning import seed_everything
import torch
import logging
import umap

from .LitPatNN_ import LitPatNN


class DMT(BaseEstimator):
    def __init__(self,
                 seed:int=1,
                 epochs:int=1500,
                 device_id:int|None=None,
                 checkpoint_path: PathLike|None="./",
                 **kwargs) -> None:
        '''
        The method explains the relationships and characteristics of the data. It can generate one-to-one, well-formed scatter plots that reveal relationships within the data. It can explain the characteristics of the data from global, local, and transfer perspectives.
        @article{zang2023evnet,
            title={Evnet: An explainable deep network for dimension reduction},
            author={Zang, Zelin and Cheng, Shenghui and Lu, Linyan and Xia, Hanchen and Li, Liangyu and Sun, Yaoting and Xu, Yongjie and Shang, Lei and Sun, Baigui and Li, Stan Z},
            journal={IEEE Transactions on Visualization and Computer Graphics},
            year={2023},
            publisher={IEEE}
        }
        Parameters
        ----------
        seed : int, optional
            Random seed, by default 1
        epochs : int, optional
            Number of epochs, by default 1500
        device_id : int, optional
            Device id, by default None
        checkpoint_path : PathLike, optional
            Checkpoint path, by default "./"
        num_fea_aim : float or -1, optional
            Proportion of target's characteristics selected, by default -1
        '''
        super().__init__()
        seed_everything(seed)
        os.makedirs(checkpoint_path, exist_ok=True)

        self._validate_parameters(epochs=epochs, device_id=device_id, checkpoint_path=checkpoint_path, **kwargs)

        if device_id is not None and device_id >= 0 and torch.cuda.is_available():
            logging.debug("Using GPU")
            torch.set_float32_matmul_precision('high')
            self.trainer = Trainer(
                accelerator="gpu",
                devices=[device_id],
                max_epochs=epochs,
                logger=False,
                default_root_dir=checkpoint_path,
                enable_checkpointing=False,
            )
            device = torch.device(f"cuda:{device_id}")
        else:
            logging.debug("Using CPU")
            self.trainer = Trainer(
                max_epochs=epochs,
                logger=False,
                default_root_dir=checkpoint_path,
            )
            device = torch.device("cpu")
        self.model = LitPatNN(device=device, epochs=epochs, **kwargs)

    def _validate_parameters(self, **kwargs):
        if kwargs['device_id'] is not None and (kwargs['device_id'] < 0 or kwargs['device_id'] >= torch.cuda.device_count()):
            raise ValueError("device_id must be greater than or equal to 0 and less than the number of GPUs")
        if kwargs['epochs'] < 10:
            raise ValueError("epochs must be greater than or equal to 10")
        if kwargs['num_fea_aim'] < -1:
            raise ValueError("num_fea_aim must be greater than or equal to -1")
        if 'metric' in kwargs and kwargs['metric'] not in ['euclidean', 'cossim']:
            raise ValueError("metric must be 'euclidean' or 'cossim'")
        if kwargs['num_fea_aim'] != -1 and kwargs['num_fea_aim'] < 0 or kwargs['num_fea_aim'] > 1:
            raise ValueError("num_fea_aim must be greater than or equal to -1 and less than or equal to 1")

    def fit_transform(self, X:np.ndarray|torch.Tensor) -> np.ndarray:
        '''
        Fit the model and transform the input data
        Parameters
        ----------
        X : np.ndarray or torch.Tensor
            The input data
        Returns
        -------
        np.ndarray
            The transformed data
        '''
        
        if not isinstance(X, np.ndarray) and not isinstance(X, torch.Tensor):
            raise ValueError("X must be a numpy array or a torch tensor")

        self.model.adapt(X)
        self.trainer.fit(self.model)
        _, _, lat3 = self.model(torch.tensor(X).float())
        return lat3.cpu().detach().numpy()

    def fit(self, X):
        '''
        Fit the model
        Parameters
        ----------
        X : np.ndarray or torch.Tensor
            The input data
        '''
        if not isinstance(X, np.ndarray) and not isinstance(X, torch.Tensor):
            raise ValueError("X must be a numpy array or a torch tensor")

        self.model.adapt(X)
        self.trainer.fit(self.model)
        
    def transform(self, X):
        '''
        Transform the input data
        Parameters
        ----------
        X : np.ndarray or torch.Tensor
            The input data
        Returns
        -------
        np.ndarray
            The transformed data
        '''
        if not isinstance(X, np.ndarray) and not isinstance(X, torch.Tensor):
            raise ValueError("X must be a numpy array or a torch tensor")
        _, _, lat3 = self.model(torch.tensor(X).float())
        return lat3.cpu().detach().numpy()
    
    def compare(self, X, plot=None):
        '''
        Compare the embeddings of DMT-EV, UMAP, TSNE and PCA
        Parameters
        ----------
        X : np.ndarray or torch.Tensor
            The input data
        plot : str, optional
            The path to save the plot, by default None
        Returns
        -------
        tuple
            The embeddings of DMT-EV, UMAP, TSNE and PCA
        '''
                
        if not isinstance(X, np.ndarray) and not isinstance(X, torch.Tensor):
            raise ValueError("X must be a numpy array or a torch tensor")

        logging.debug("Start DMT-EV")
        dmt_embedding = self.fit_transform(X)
        logging.debug("Start UMAP")
        umap_embedding = umap.UMAP().fit_transform(X)
        logging.debug("Start TSNE")
        tsne_embedding = TSNE().fit_transform(X)
        logging.debug("Start PCA")
        pca_embedding = PCA().fit_transform(X)
        
        if plot:
            logging.debug("Plotting")
            if not isinstance(plot, str):
                raise ValueError("plot must be a path")
            if len(os.path.dirname(plot)) > 0 and not os.path.exists(os.path.dirname(plot)):
                os.makedirs(os.path.dirname(plot))
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 4, figsize=(20, 5))
            ax[0].scatter(dmt_embedding[:, 0], dmt_embedding[:, 1])
            ax[0].set_title("DMT")
            ax[1].scatter(umap_embedding[:, 0], umap_embedding[:, 1])
            ax[1].set_title("UMAP")
            ax[2].scatter(tsne_embedding[:, 0], tsne_embedding[:, 1])
            ax[2].set_title("TSNE")
            ax[3].scatter(pca_embedding[:, 0], pca_embedding[:, 1])
            ax[3].set_title("PCA")
            plt.savefig(plot)

        return dmt_embedding, umap_embedding, tsne_embedding, pca_embedding
    
