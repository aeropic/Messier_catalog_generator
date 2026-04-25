# Messier_catalog_generator
This is a python script to build a catalog of your Messier's object astrophotographies

I'd been wanting to manage the (pathetic!) progress of my Messier catalog for a while.

I searched the web for a simple tool to create a clickable contact sheet, and since I didn't find anything, here's a little Python script that does the job.

Simply organize your image files in a folder and add the string "M1, M2 ... Mxyz" to the image names.

Place the "Messier_generator.py" script and the "Messier.bat" file in the same folder. Double-click on Messier.bat, accept the Windows prompts, and it generates an interactive HTML contact sheet.

- The thumbnails are clickable to access the zoomable image.

The marathon score is displayed at the top (for me, it's like a leisurely stroll with 32 in 2 years!).

If there are multiple objects in the same image, name the file with both objects (e.g., M65_M66_triplet_lion.jpg).
The script includes a mini-catalog, and the object type is indicated below the object number. I was surprised to see that mischievous Messier slipped a double star into M40 and something odd into M24!

The .bat file, of course, only runs on PC...

Let me know if it works for you too and if you see any improvements you could make! And post your scores here!

Note: Open the .bat file and specify the path to your Python installation. I pointed to SIRIL's path:
:: Launch Python on the script located in the same folder:
"C:\Program Files\Siril\python\python.exe" "Messier_generator.py"

You can easily translate the script in any langage as all strings are gathered at the top of the script... Meanwhile in french !
