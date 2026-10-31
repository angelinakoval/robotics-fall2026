# mission_1

## diagnosis
normal_1: the box is on the mug, but slightly shifted to the right and extended downward.  In the raw threshold mask, the mug body and its shadow on the table were merged into one white region, due to the similarity in colors (mug and its shadow on the table)
dim_1: the box is not on the mug at all. It covers the shadow of the mug and a small area of the mug's bottom part. In dim image is darker -> many mug pixels were below 45 (minimum value)

## limitations
I changed hue and dropped it from 35 to 12. This reduced the size of the box, because the rule now includes less of the orange shades (mostly reddish-brown shades remain), and therefore includes less of the table area.
Limitation:the rule works only for the specific colors in this image. If the color of the cup or the background (table) changes, the results will be different
