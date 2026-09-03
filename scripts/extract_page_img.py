import sys, io, os

sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader
from PIL import Image

SRC = r"C:\Users\JKer\Desktop\祝由十三科.pdf"


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
    # 用法: python extract_page_img.py 5 输出目录
    pno = int(sys.argv[1])
    outdir = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.join(
            os.environ["USERPROFILE"], "Desktop", "祝由十三科-应答档案", "_原书页图"
        )
    )
    fn = save_page(pno, outdir)
    print(fn or "no image on this page")
