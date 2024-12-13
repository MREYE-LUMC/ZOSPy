# Modelling of a Shack-Hartmann Sensor for eye aberration evaluation

This example covers the knowledgebase tutorial [Modelling of a Shack-Hartmann Sensor for eye aberration evaluation](https://support.zemax.com/hc/en-us/articles/4406838460819-Modelling-of-a-Shack-Hartmann-Sensor-for-eye-aberration-evaluation)   using ZOSPy to control the API. It gives a step-by-stp explanation of all used steps. 

In addition, it addressed an error made in the gradient index of the crystalline lens in the original knowledgebase example. In [the original example](1_Model_SH_original.ipynb), the gradient index of the crystalline lens was indirectly reverted when creating an reverted eye model. To solve this, we [first fit the correct inverted gradient index](2_Fitting_reverse_gradient_3.ipynb)and then implement that gradient in an [updated version of the knowledgebase example](3_Model_SH_updated.ipynb)

```{toctree}
:maxdepth: 1

1_Model_SH_original
2_Fitting_reverse_gradient_3
3_Model_SH_updated
```
