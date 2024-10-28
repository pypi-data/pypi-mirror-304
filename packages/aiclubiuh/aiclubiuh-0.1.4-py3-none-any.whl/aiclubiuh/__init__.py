# aiclubiuh/__init__.py

# def show_info():
#     info = """
#     **AI_Club - Câu lạc bộ Trí tuệ nhân tạo IUH**

#     **Hoạt động chính:**
#     - Học và tham gia các khóa miễn phí về Lập trình, Toán, AI.
#     - Nghiên cứu khoa học, dự hội nghị.
#     - Hoạt động giải trí: văn nghệ, thể thao.

#     **Trang thiết bị:**
#     - Phòng lab hiện đại tại Data Innovation Lab H2.2, Trường Đại học Công nghiệp TP.HCM.

#     **Đối tượng:**
#     - Sinh viên đam mê AI, khoa học dữ liệu, không phân biệt ngành.

#     **Lý do tham gia:**
#     - Học từ giảng viên, mentor; tham gia các cuộc thi lớn.
#     - Hỗ trợ nghiên cứu khoa học.
#     - Tham gia workshop, seminar và các hoạt động gắn kết.
#     - Cơ hội học hỏi kinh nghiệm từ các anh chị khóa trước.

#     Cùng tham gia để phát triển và khám phá!
#     """
#     print(info)

# show_info()


from rich.console import Console
from rich.markdown import Markdown

def introduce():
    intro_text = """
**AI_Club - Câu lạc bộ Trí tuệ nhân tạo IUH**

**Hoạt động chính:**
- Học và tham gia các khóa miễn phí về Lập trình, Toán, AI.
- Nghiên cứu khoa học, dự hội nghị.
- Hoạt động giải trí: văn nghệ, thể thao.

**Trang thiết bị:**
- Phòng lab hiện đại tại Data Innovation Lab H2.2, Trường Đại học Công nghiệp TP.HCM.

**Đối tượng:**
- Sinh viên đam mê AI, khoa học dữ liệu, không phân biệt ngành.

**Lý do tham gia:**
- Học từ giảng viên, mentor; tham gia các cuộc thi lớn.
- Hỗ trợ nghiên cứu khoa học.
- Tham gia workshop, seminar và các hoạt động gắn kết.
- Cơ hội học hỏi kinh nghiệm từ các anh chị khóa trước.

Cùng tham gia để phát triển và khám phá!
    """
    console = Console()
    markdown = Markdown(intro_text)
    console.print(markdown)

# Khi import, tự động gọi hàm introduce
introduce()