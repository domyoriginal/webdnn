import numpy as np

from test.runtime.frontend_test.keras_test.util import keras, KerasConverter
from test.util import generate_kernel_test_case, wrap_template


@wrap_template
def template(shape=(14, 15, 4), filters=5, kernel_size=3, strides=(1, 1), padding='valid', data_format="channels_last",
             dilation_rate=(1, 1), activation=None, use_bias=True, description: str = ""):
    x = keras.layers.Input(shape)
    y = keras.layers.Conv2DTranspose(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding, data_format=data_format,
                                     dilation_rate=dilation_rate, activation=activation, use_bias=use_bias)(x)
    model = keras.models.Model([x], [y])

    vx = np.random.rand(2, *shape).astype(np.float32)
    vy = model.predict(vx, batch_size=2)

    graph = KerasConverter(batch_size=2, use_tensorflow_converter=False).convert(model)

    generate_kernel_test_case(
        description=f"[keras] Conv2DTranspose {description}",
        graph=graph,
        backend=["webgpu", "webgl", "webassembly"],
        inputs={graph.inputs[0]: vx},
        expected={graph.outputs[0]: vy},

        # TODO: replace computation algorithm with more accurate one
        EPS=1e-2
    )


def test():
    template()


def test_padding_valid():
    template(padding="valid")


def test_padding_same_even_size():
    # pad: ((1,1), (1,1))
    template(padding="SAME", shape=(5, 5, 3), kernel_size=3, strides=1)


def test_padding_same_odd_size():
    # pad: ((1,0), (1,0))
    template(padding="SAME", shape=(4, 4, 3), kernel_size=2, strides=1)


def test_kernel_size():
    template(kernel_size=2)


def test_strides():
    template(strides=(2, 2))


def test_data_format():
    template(shape=(4, 14, 15), data_format="channels_first")


# TODO: Not supported yet
# def test_dilation():
#     template(shape=(14, 14, 4), dilation_rate=(2, 2))


def test_activation():
    template(activation="relu")


def test_nobias():
    template(use_bias=False)
