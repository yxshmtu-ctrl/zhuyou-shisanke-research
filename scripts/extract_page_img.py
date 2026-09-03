import sys, io, os

sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader
from PIL import Image


# 源 PDF 定位顺序：① 命令行第3参数 ② 环境变量 ZHUYOU_SRC ③ 本脚本同级向上找 祝由十三科.pdf
def find_source_pdf():
    cands = []
    if len(sys.argv) > 3:
        cands.append(sys.argv[3])
    if os.environ.get("ZHUYOU_SRC"):
        cands.append(os.environ["ZHUYOU_SRC"])
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.join(here, "..", "祝由十三科.pdf"))
    cands.append(os.path.join(here, "..", "..", "祝由十三科.pdf"))
    cands.append(os.path.join(os.path.expanduser("~"), "Desktop", "祝由十三科.pdf"))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


SRC = find_source_pdf()


def extract_page_image(pg):
    """从 PDF 页面取回扫描图像 PIL.Image"""
    xo = pg["/Resources"]["/XObject"]
    for k in xo:
        o = xo[k].get_object()
        if o.get("/Subtype") == "/Image":
            return Image.open(io.BytesIO(o.get_data()))
    return None


def save_page(pdf_page_no, outdir):
    """pdf_page_no 从1开始。保存为 pNNN.png 到 outdir，返回保存路径。"""
    reader = PdfReader(SRC)
    pg = reader.pages[pdf_page_no - 1]
    img = extract_page_image(pg)
    if img is None:
        return None
    os.makedirs(outdir, exist_ok=True)
    fn = os.path.join(outdir, f"p{pdf_page_no:03d}.png")
    img.save(fn)
    return fn


if __name__ == "__main__":
    # 用法: python extract_page_img.py <页码> [输出目录] [源PDF]
    # 页码从1开始。源PDF缺省时自动查找（见 find_source_pdf）
    pno = int(sys.argv[1])
    outdir = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.join(
            os.environ.get("USERPROFILE", os.path.expanduser("~")),
            "Desktop",
            "祝由十三科-应答档案",
            "_原书页图",
        )
    )
    if SRC is None:
        print("ERROR: 未找到源 PDF。请用第3参数指定，或设环境变量 ZHUYOU_SRC")
        sys.exit(1)
    fn = save_page(pno, outdir)
    print(fn or "no image on this page")
