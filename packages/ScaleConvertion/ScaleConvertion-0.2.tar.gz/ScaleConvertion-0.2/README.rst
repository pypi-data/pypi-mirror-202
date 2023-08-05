ScaleConvertion
-----------------------------------------------------------------

ResTransformer-based surface reflectance scale conversion tool

.. code:: python

    from ScaleConvertion.PicProcess.Draw_Window import read_
    from ScaleConvertion.main import getSeds

    if __name__ == '__main__':
        img_path = r""
        save_dir = "tmp"
        a, b = getSeds()
        read_(img_path, save_dir, a, sensors_altitude=b, pixel=[2, 4, 8, 10, 20, 30])
