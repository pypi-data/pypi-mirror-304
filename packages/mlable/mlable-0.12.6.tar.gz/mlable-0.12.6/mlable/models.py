import tensorflow as tf

import mlable.masking

# CONTRAST #####################################################################

class ContrastModel(tf.keras.models.Model):
    def compute_loss(
        self,
        x: tf.Tensor=None,
        y: tf.Tensor=None,
        y_pred: tf.Tensor=None,
        sample_weight: tf.Tensor=None,
    ):
        __loss = super(ContrastModel, self).compute_loss(x, y, y_pred, sample_weight)
        __weights = mlable.masking.contrast(left=x, right=tf.cast(tf.argmax(y, axis=-1), dtype=x.dtype), weight=0.9, dtype=__loss.dtype)
        return __weights * __loss
