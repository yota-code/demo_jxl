https://www.levien.com/artofcode/fontfocus/compare.html
https://blog.gtk.org/2024/03/07/on-fractional-scales-fonts-and-hinting/


If you want an ideal case scenario for JXL, then upscaled pixel art is very hard to beat.
You resize the art back down to 1:1 pixels, then with lossless you add
`--already_downsampled --resampling=(2, 4 or 8, whichever is closest to the original) --upsampling_mode=0`
All the benefits of a tiny image, with the readability of a file 8x the size. I *technically* hit 0.3 bpp with it losslessly
