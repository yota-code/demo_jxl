https://www.levien.com/artofcode/fontfocus/compare.html
https://blog.gtk.org/2024/03/07/on-fractional-scales-fonts-and-hinting/


If you want an ideal case scenario for JXL, then upscaled pixel art is very hard to beat.
You resize the art back down to 1:1 pixels, then with lossless you add
`--already_downsampled --resampling=(2, 4 or 8, whichever is closest to the original) --upsampling_mode=0`
All the benefits of a tiny image, with the readability of a file 8x the size. I *technically* hit 0.3 bpp with it losslessly

https://ariya.io/2016/06/using-zopfli-to-optimize-png-images


For a file of 485954 bytes ./forge/zopfli/zopflipng --iterations=<n> --filters=01234mepb --lossy_transparent <in>.png <out>.png
16	323341	39,83s user 0,04s system 99% cpu 39,881 total
32	323306	70,97s user 0,11s system 87% cpu 1:21,60 total
48	323298	101,26s user 0,07s system 90% cpu 1:51,69 total
64	323296	130,93s user 0,10s system 60% cpu 3:36,44 total


https://github.com/shssoichiro/oxipng

https://github.com/fhanau/Efficient-Compression-Tool

http://www.olegkikin.com/png_optimizers/

https://css-ig.net/benchmark/png-lossless


for pixel art : d0e10P0I0

ect -strip -99999 --mt-deflate --allfilters-b --pal_sort=120