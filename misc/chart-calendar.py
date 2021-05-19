import heniautos as ha
import argparse
import matplotlib.pyplot as plt
import sys

# Color constants
CLR = {"F": "#40B0A6",
       "H": "#E1BE6A",
       "?": "#FFFFFF"}

MONTH_LABELS = ("He", "Me", "Bo", "Pu", "Ma", "Po",
                "Ga", "An", "El", "Mo", "Th", "Sk")

PRYTANY_LABELS = ("I", "II", "III", "IV", "V", "VI", "VII",
                  "VIII", "IX", "X", "XI", "XII", "XIII")


def fest_width(m):
    if m in ("F", "I", "?"):
        return 300

    return 290


def fest_hatch(m):
    if m in ("f", "h", "?"):
        return "///"

    if m in ("I", "i"):
        return ".."

    return None


def fest_color(m):
    if m in ("F", "f", "I"):
        return CLR["F"]

    if m in ("H", "h", "i"):
        return CLR["H"]

    return CLR["?"]


def pryt_width(m, cnt, is_ordinary):
    if cnt == 10:
        if m in ("F", "f"):
            return 360 if is_ordinary else 390

        return 350 if is_ordinary else 380

    if cnt == 12:
        if is_ordinary:
            return 300 if m in ("F", "f") else 290

        return 320

    if cnt == 13:
        if m in ("F", "f"):
            return 280 if is_ordinary else 300

        return 270 if is_ordinary else 290

    raise Exception("UNHANDLED")


def month_label(i, pat):
    if pat in ("I", "i"):
        return None

    return MONTH_LABELS[i]


def chart_festival_boxes(ax, pat, x, y, cnt, label_months):
    if not pat:
        return

    ax.add_patch(plt.Rectangle((x, y),
                               fest_width(pat[0]), -300,
                               fc = fest_color(pat[0]), 
                               ec="#000000",
                               hatch = fest_hatch(pat[0])))

    if label_months:
        ax.text(x + fest_width(pat[0])/2, y-150,
                month_label(cnt, pat[0]),
                ha="center", va="center", fontsize=8, fontweight="bold",
                fontname="Arial", backgroundcolor=None,
                bbox={"fill": False, "lw": 0, "pad": 0})

    chart_festival_boxes(ax, pat[1:], x + fest_width(pat[0]), y,
                         cnt if pat[0] in ("I", "i") else cnt + 1,
                         label_months)


def chart_conciliar_boxes(ax, pat, pryt_cnt, is_ordinary, x, y, labels):
    if not pat:
        return

    ax.add_patch(plt.Rectangle((x, y),
                               pryt_width(pat[0], pryt_cnt, is_ordinary), -300,
                               fc = fest_color(pat[0]), 
                               ec="#000000",
                               hatch = fest_hatch(pat[0])))
    
    if labels:
        ax.text(x + pryt_width(pat[0], pryt_cnt, is_ordinary)/2, y-150,
                labels[0],
                ha="center", va="center", fontsize=8, fontweight="bold",
                fontname="Arial", backgroundcolor=None,
                bbox={"fill": False, "lw": 0, "pad": 0})

    chart_conciliar_boxes(ax, pat[1:], pryt_cnt, is_ordinary,
                          x + pryt_width(pat[0], pryt_cnt, is_ordinary), y,
                          labels[1:] if labels else None)


def chart_cal_boxes_label(ax, label, x, y):
    ax.text(x-150, y-150, label, ha="center", va="center", fontsize=10,
            fontname="Arial",
            backgroundcolor=None, bbox={"fill": False, "lw": 0, "pad": 0})
    

def chart_festival_row(ax, fest_pat, x, y, label_months):
    chart_festival_boxes(ax, fest_pat, x, y, 0, label_months)
    chart_cal_boxes_label(ax, "F", x, y)


def chart_conciliar_row(ax, conc_pat, is_ordinary, x, y, label_months,
                        pryt_cnt):
    chart_conciliar_boxes(ax, conc_pat, pryt_cnt, is_ordinary, x, y,
                          PRYTANY_LABELS if label_months else None)
        
    chart_cal_boxes_label(ax, "C", x, y)


def chart_partitions(ax, partitions, fest_pat, is_both, x, y):
    if not partitions:
        return

    pos = sum([300 if m in ("F", "I", "?") else 290
               for m in fest_pat[:partitions[0]]])

    if is_both:
        ax.arrow(x + pos , y+200, 0, -1100, linestyle="dotted", head_width=0)
    else:
        ax.arrow(x + pos , y+200, 0, -700, linestyle="dotted", head_width=0)

    chart_partitions(ax, partitions[1:], fest_pat, is_both, x, y)
             
    
    

def chart_example(ax, fest_pat, conc_pat, label, label_months, show_festival,
                  show_conciliar, pryt_cnt, is_intercalary, partitions=[],
                  x=0, y=0):
    """Chart given example patterns."""
    if show_festival and not fest_pat or show_conciliar and not conc_pat:
        return y

    if show_festival:
        chart_festival_row(ax, fest_pat[0].replace(" ", ""),
                           x, y, label_months)

    if show_conciliar and conc_pat:
        chart_conciliar_row(ax, conc_pat[0].replace(" ", ""),
                            not is_intercalary, x, y-400, label_months,
                            pryt_cnt)

    if label[0] is not None:
        fmt_label = "\n".join(label[0].split("|"))

        if show_festival and show_conciliar:
            ax.add_patch(plt.Rectangle(
                (x-1200, y), 900, -700, fc = "white", ec="#000000"))
        
            ax.text(x-750, y-350, fmt_label, ha="center", va="center",
                    fontsize=10, backgroundcolor=None,
                    bbox={"fill": False, "lw": 0, "pad": 0})
        else:
            ax.add_patch(plt.Rectangle(
                (x-1200, y), 900, -300, fc = "white", ec="#000000"))
        
            ax.text(x-750, y-150, fmt_label, ha="center", va="center",
                    fontsize=10, backgroundcolor=None,
#                    fontname="Arial",
                    bbox={"fill": False, "lw": 0, "pad": 0})


    if partitions:
        chart_partitions(ax, partitions, fest_pat[0],
                         show_festival and show_conciliar, x, y)

    if show_festival and show_conciliar:
        return chart_example(ax, fest_pat[1:], conc_pat[1:], label[1:],
                             label_months, show_festival, show_conciliar,
                             pryt_cnt, is_intercalary, partitions,
                             x, y-1400)
    elif show_festival:
        return chart_example(ax, fest_pat[1:], conc_pat, label[1:],
                             label_months, show_festival, show_conciliar,
                             pryt_cnt, is_intercalary, partitions,
                             x, y-700)
    else:
        return chart_example(ax, fest_pat, conc_pat[1:], label[1:],
                             label_months, show_festival, show_conciliar,
                             pryt_cnt, is_intercalary, partitions,
                             x, y-700)
            

def fh(m):
    if m["constant"] == ha.Months.INT:
        if len(m["days"]) == 30:
            return "I"

        return "i"

    if len(m["days"]) == 30:
        return "F"

    return "H"


def fh_pryt(p, short, lng=None):
    if lng is None or len(p["days"]) == lng:
        return "F"

    return "H"

            
def get_festival_pattern(year):
    return "".join([fh(m) for m
                    in ha.festival_calendar(ha.bce_as_negative(year))])


def get_conciliar_pattern(year, fest_pat):
    pryt = ha.prytany_calendar(ha.bce_as_negative(year))

    if len(pryt) == 10:
        return "F"*4 + "H"*6

    if len(pryt) == 12:
        if len(fest_pat) == 12:
            return fest_pat

        return "F"*12

    if len(pryt) == 13:
        if len(fest_pat) == 13:
            return fest_pat.replace("I", "F").replace("i", "h")

        return "F"*3 + "H"*10


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int)
    parser.add_argument("--festival", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="Include festival year chart")
    parser.add_argument("--conciliar", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="Include conciliar year chart")
    parser.add_argument("--festival-pattern", metavar="PATTERN", type=str,
                        nargs="+",
                        help="Pattern of full and hollow months to chart. "
                        "Use 'F' for full (30-day) and 'H' for hollow "
                        "(29-day). If you want to specify an intercalary "
                        "use 'I' for a 30-day, 'i' for a 29-day "
                        "intercalation.")
    parser.add_argument("--conciliar-pattern", metavar="PATTERN", type=str,
                        nargs="+")
    parser.add_argument("--label-months", type=bool, default=False,
                        action=argparse.BooleanOptionalAction,
                        help="Add labels for months to festival month chart")
    parser.add_argument("--label", type=str, nargs="+")
    parser.add_argument("-p", "--prytanies", type=int, default=10)
    parser.add_argument("-i", "--intercalary", action="store_true")
    parser.add_argument("--partitions", type=int, nargs="+")
    parser.add_argument("-o", "--output",
                        help="Save chart to file")
    parser.add_argument("-e", "--ephemeris", metavar="FILE", type=str,
                        help="Use existing ephemeris FILE (if it cannot "
                        "automatically be found)", default=None)
    args = parser.parse_args()

    fig, ax = plt.subplots()

    if args.year:
        ha.init_data(args.ephemeris)
        fest_pat = get_festival_pattern(args.year)
        max_y = chart_example(
            ax,
            [fest_pat],
            [get_conciliar_pattern(args.year, fest_pat)],
            args.label if args.label else [str(args.year)],
            args.label_months, args.festival, args.conciliar,
            ha.phulai_count(ha.bce_as_negative(args.year)),
            len(fest_pat) == 13,
            args.partitions)

    if args.festival_pattern or args.conciliar_pattern:
        max_y = chart_example(
            ax,
            args.festival_pattern,
            args.conciliar_pattern,
            [None]*len(args.festival_pattern) if args.label is None else \
            args.label,
            args.label_months,
            args.festival,
            args.conciliar,
            args.prytanies,
            args.intercalary,
            args.partitions)

    ax.autoscale()
#    ax.set_xticks([])
#    ax.set_yticks([])
    ax.set_aspect(1)
    plt.axis("off")

    if args.output:
        plt.savefig(args.output, dpi=900, bbox_inches="tight")
    else:
        plt.show()
