import chainer
import numpy as np

from test.util import generate_kernel_test_case, wrap_template
from webdnn.frontend.chainer.converter import ChainerConverter


@wrap_template
def template(description: str = ""):
    vx = chainer.Variable(np.random.rand(2, 5, 6, 8).astype(np.float32) * 2 - 1)  # domain: [-1, 1]
    vy = chainer.functions.arccos(vx)

    graph = ChainerConverter().convert([vx], [vy])

    x = graph.inputs[0]
    y = graph.outputs[0]

    generate_kernel_test_case(
        description=f"[chainer] F.arccos {description}",
        graph=graph,
        inputs={x: vx.data},
        expected={y: vy.data},
        EPS=1e-2
    )


def test():
    template()
