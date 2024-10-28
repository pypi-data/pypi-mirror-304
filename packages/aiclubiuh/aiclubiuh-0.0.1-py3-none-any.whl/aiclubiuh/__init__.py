from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

def introduce():
    intro_text = """
**AI_Club - Câu lạc bộ Trí tuệ nhân tạo IUH**

Câu lạc bộ Trí tuệ Nhân tạo (AI Club) tại Trường Đại học Công nghiệp TP.HCM được thành lập từ năm 2019, tọa lạc tại phòng Data Innovation Lab H2.2. Đây là nơi dành cho các sinh viên yêu thích và đam mê nghiên cứu trong lĩnh vực Khoa học Dữ liệu (KHDL) và Khoa học Máy tính (KHMT), tạo ra một môi trường học tập năng động và sân chơi học thuật để phát triển kỹ năng và kiến thức chuyên môn.

**Hoạt động chính:**
- Tham gia các khóa học miễn phí về Lập trình, Toán học, Trí tuệ Nhân tạo.
- Nghiên cứu khoa học và tham dự hội nghị.
- Tham gia các hoạt động giải trí như văn nghệ và thể thao.

**Trang thiết bị:**
- Phòng lab hiện đại tại Data Innovation Lab H2.2, Trường Đại học Công nghiệp TP.HCM.

**Đối tượng:**
- Tất cả sinh viên đam mê AI, khoa học dữ liệu, không phân biệt ngành học.

**Lý do tham gia:**
- Học hỏi từ giảng viên, mentor và tham gia các cuộc thi lớn.
- Tham gia các workshop, seminar và các hoạt động kết nối.
- Cơ hội học hỏi kinh nghiệm từ các anh chị khóa trước.

Hãy cùng tham gia AI Club để phát triển bản thân và khám phá những tiềm năng mới!
    """
    console = Console()
    markdown = Markdown(intro_text)
    panel = Panel(markdown, title="🎓 AI_Club IUH 🎓", expand=False, border_style="bold green")
    console.print(panel)

introduce()
