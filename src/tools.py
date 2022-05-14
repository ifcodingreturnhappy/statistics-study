import sys

# Credits to:
#               https://stackoverflow.com/a/34482761
#


def progressbar(it, prefix="", bar_size=60, out=sys.stdout, delete_bar_on_complete=True):  # Python3.3+
    count = len(it)

    def show(j):
        x = int(bar_size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, u"█"*x, "."*(bar_size-x), j, count),
              end='\r', file=out, flush=True)

        if(j == count and delete_bar_on_complete):
            out.write("\033[F")  # Cursor up one line
            out.write("\033[F")  # Cursor up one line

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
