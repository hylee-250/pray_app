from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from models import Base, Prayer
from datetime import datetime, timedelta
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, Alignment
import io
import os

# ✅ FastAPI 앱 인스턴스 생성
app = FastAPI()

# ✅ Jinja 템플릿 설정
templates = Jinja2Templates(directory="templates")

# ✅ DB 초기화
Base.metadata.create_all(bind=engine)

# 하드코딩된 다락방과 순장 관계 (실제로는 설정 페이지에서 관리)
CELL_GROUP_LEADERS = {
    "은혜다락방": [
        "고영은",
        "김다빈",
        "송은설",
        "오지은",
        "이호영",
        "용민기",
        "최다열",
        "이용식",
    ],
    "하품다락방": [
        "하품1",
        "하품2",
        "하품3",
        "하품4",
        "하품5",
        "하품6",
        "하품7",
        "하품8",
    ],
    "오지다락방": [
        "오지1",
        "오지2",
        "오지3",
        "오지4",
        "오지5",
        "오지6",
        "오지7",
        "오지8",
    ],
    "소금다락방": [
        "소금1",
        "소금2",
        "소금3",
        "소금4",
        "소금5",
        "소금6",
        "소금7",
        "소금8",
    ],
    "새가족다락방": [
        "새가족1",
        "새가족2",
        "새가족3",
        "새가족4",
        "새가족5",
        "새가족6",
        "새가족7",
        "새가족8",
    ],
}


@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "cell_groups": list(CELL_GROUP_LEADERS.keys()),
            "cell_group_leaders": CELL_GROUP_LEADERS,
        },
    )


@app.get("/api/leaders/{cell_group}")
def get_leaders_by_cell_group(cell_group: str):
    return {"leaders": CELL_GROUP_LEADERS.get(cell_group, [])}


@app.post("/submit")
def submit_prayer(
    request: Request,
    name: str = Form(...),
    leader: str = Form(...),
    cell_group: str = Form(...),
    content: str = Form(...),
):
    db = SessionLocal()
    new_prayer = Prayer(
        name=name,
        leader=leader,
        cell_group=cell_group,
        content=content,
        created_at=datetime.now(),
    )
    db.add(new_prayer)
    db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)


def get_week_range(week_offset=0):
    """현재 날짜를 기준으로 일요일~토요일 범위를 반환"""
    today = datetime.now()
    # 일요일이 0, 토요일이 6이 되도록 조정
    days_since_sunday = today.weekday() + 1  # weekday()는 월요일이 0이므로 +1
    if days_since_sunday == 7:  # 일요일인 경우
        days_since_sunday = 0

    sunday = today - timedelta(days=days_since_sunday)
    sunday = sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    # 주차 오프셋 적용
    sunday += timedelta(weeks=week_offset)
    saturday = sunday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return sunday, saturday


def get_week_label(week_offset=0):
    """주차 라벨 생성 (예: 7월 27일~8월 2일)"""
    sunday, saturday = get_week_range(week_offset)

    # 같은 월인 경우
    if sunday.month == saturday.month:
        return f"{sunday.month}월 {sunday.day}일~{saturday.day}일"
    # 다른 월인 경우
    else:
        return f"{sunday.month}월 {sunday.day}일~{saturday.month}월 {saturday.day}일"


@app.get("/admin")
def view_all(
    request: Request,
    leader: str = Query(default=None),
    cell_group: str = Query(default=None),
    week_offset: int = Query(default=0),
):
    db = SessionLocal()

    # 주차 필터 적용 (일요일~토요일)
    week_start, week_end = get_week_range(week_offset)
    prayers = (
        db.query(Prayer)
        .filter(Prayer.created_at >= week_start, Prayer.created_at <= week_end)
        .order_by(Prayer.created_at.desc())
        .all()
    )
    db.close()

    unique_leaders = sorted(set(str(p.leader) for p in prayers if p.leader))
    unique_cell_groups = sorted(set(str(p.cell_group) for p in prayers if p.cell_group))

    # 필터 적용
    if leader:
        prayers = [p for p in prayers if str(p.leader) == leader]
    if cell_group:
        prayers = [p for p in prayers if str(p.cell_group) == cell_group]

    # 다락방-순장별로 그룹핑
    grouped = {}
    for p in prayers:
        cg = p.cell_group or "미지정"
        ld = p.leader or "미지정"
        if cg not in grouped:
            grouped[cg] = {}
        if ld not in grouped[cg]:
            grouped[cg][ld] = []
        grouped[cg][ld].append(p)

    # 주차 옵션 생성 (현재 주부터 이전 4주, 이후 1주)
    week_options = []
    for i in range(-4, 2):
        week_options.append(
            {"offset": i, "label": get_week_label(i), "selected": i == week_offset}
        )

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "prayers": prayers,
            "leaders": unique_leaders,
            "cell_groups": unique_cell_groups,
            "selected_leader": leader,
            "selected_cell_group": cell_group,
            "grouped": grouped,
            "week_options": week_options,
            "current_week_label": get_week_label(week_offset),
            "cell_group_leaders": CELL_GROUP_LEADERS,
        },
    )


@app.get("/export-excel")
def export_excel(
    leader: str = Query(default=None),
    cell_group: str = Query(default=None),
    week_offset: int = Query(default=0),
):
    db = SessionLocal()

    # 주차 필터 적용 (일요일~토요일)
    week_start, week_end = get_week_range(week_offset)
    prayers = (
        db.query(Prayer)
        .filter(Prayer.created_at >= week_start, Prayer.created_at <= week_end)
        .order_by(Prayer.created_at.desc())
        .all()
    )
    db.close()

    # 필터 적용
    if leader:
        prayers = [p for p in prayers if str(p.leader) == leader]
    if cell_group:
        prayers = [p for p in prayers if str(p.cell_group) == cell_group]

    # 다락방-순장별로 그룹핑
    grouped = {}
    for p in prayers:
        cg = p.cell_group or "미지정"
        ld = p.leader or "미지정"
        if cg not in grouped:
            grouped[cg] = {}
        if ld not in grouped[cg]:
            grouped[cg][ld] = []
        grouped[cg][ld].append(p)

    # 엑셀 워크북 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    if ws is None:
        ws = wb.create_sheet("기도제목 목록")
    else:
        ws.title = "기도제목 목록"

    # 스타일 설정
    cell_group_font = Font(size=16, bold=True)
    leader_font = Font(size=14, bold=True)
    member_font = Font(size=12, bold=True)
    content_font = Font(size=11)

    # 주차 정보 추가
    week_label = get_week_label(week_offset)
    ws.cell(row=1, column=1, value=f"기간: {week_label}")
    ws.cell(row=1, column=1).font = Font(size=14, bold=True)

    row = 3
    for cell_group, leaders in grouped.items():
        # 다락방 제목
        ws.cell(row=row, column=1, value=cell_group)
        ws.cell(row=row, column=1).font = cell_group_font
        row += 1

        for leader, prayers in leaders.items():
            # 순장 제목
            ws.cell(row=row, column=2, value=f"{leader} 순장")
            ws.cell(row=row, column=2).font = leader_font
            row += 1

            for p in prayers:
                # 순원 이름
                ws.cell(row=row, column=3, value=p.name)
                ws.cell(row=row, column=3).font = member_font
                # 기도제목 내용
                ws.cell(row=row, column=4, value=p.content)
                ws.cell(row=row, column=4).font = content_font
                row += 1

    # 파일 저장
    filename = (
        f"기도제목목록_{week_label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )
    filepath = f"./static/{filename}"

    # static 폴더가 없으면 생성
    os.makedirs("./static", exist_ok=True)

    wb.save(filepath)

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.delete("/prayer/{prayer_id}")
def delete_prayer(prayer_id: int):
    db = SessionLocal()
    prayer = db.query(Prayer).filter(Prayer.id == prayer_id).first()

    if not prayer:
        db.close()
        return {"error": "기도제목을 찾을 수 없습니다."}

    db.delete(prayer)
    db.commit()
    db.close()

    return {"message": "기도제목이 삭제되었습니다."}


@app.put("/prayer/{prayer_id}")
def update_prayer(
    prayer_id: int,
    name: str = Form(...),
    leader: str = Form(...),
    cell_group: str = Form(...),
    content: str = Form(...),
):
    db = SessionLocal()
    prayer = db.query(Prayer).filter(Prayer.id == prayer_id).first()

    if not prayer:
        db.close()
        return {"error": "기도제목을 찾을 수 없습니다."}

    # 기도제목 정보 업데이트
    prayer.name = name
    prayer.leader = leader
    prayer.cell_group = cell_group
    prayer.content = content

    db.commit()
    db.close()

    return {"message": "기도제목이 수정되었습니다."}
