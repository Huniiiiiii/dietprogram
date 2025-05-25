// ====================== 기본 element 저장 시작======================
const searchForm = document.getElementById('searchForm');
const resultBody = document.getElementById('body');
const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');
const editInput = document.getElementById('editInput');
// ======================기본 element 저장 종료======================

// ======================수정 및 삭제 행 변수 선언======================
let editingRow = null;
let deletingRow = null;


// ======================쿠키 불러오기 함수 시작======================
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
// ======================쿠키 불러오기 함수 종료======================

// ======================페이지 로드 부분 시작======================

// DOM 로드 시, 사용자의 최근 식단 표시
document.addEventListener('DOMContentLoaded', async function () {
    // let userId = getCookie('user_id');  // 쿠키에서 user_id 가져오기
    let userId = "{{ user_id }}";
    if (!userId) {
        // 현재는 쿠키에 없으면 강제로 1로 설정
        userId = '1';
        alert('로그인이 필요합니다. (임시로 user_id=1 사용)');
    }
    const response = await fetch('/modify/list', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id:userId})
    });
    const data = await response.json();

    if (data.length > 0) {
        document.getElementById('resultArea').style.display = 'block';
        const body = document.getElementById('body');
        body.innerHTML = '';

        data.forEach(meal => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="d-flex justify-content-between">
                    <div>
                        <div><strong>${meal.menu}</strong></div>
                        <div class="text-muted small">${new Date(meal.date).toLocaleDateString('ko-KR')}</div>
                        <div class="text-muted small">${meal.time}</div>
                    </div>
                    <div class="d-flex align-items-center" style="gap: 0.5rem;">
                        <button class="btn btn-primary btn-circle btn-sm" onclick="editMeal(${meal.id}, this)">
                            <i class="fas fa-pen"></i>
                        </button>
                        <button class="btn btn-danger btn-circle btn-sm" onclick="deleteMeal(${meal.id}, this)">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    </div>
                </td>
                `;

            body.appendChild(row);
        });
        
    }
});
// ======================페이지 로드 부분 종료======================

// ======================식단 조회 부분 시작======================
// 조회버튼 클릭 시 호출 함수 
searchForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const year = document.getElementById('searchYear').value;
    const month = document.getElementById('searchMonth').value;
    const day = document.getElementById('searchDay').value;
    const time = document.getElementById('searchTime').value;
    user_id = "{{ user_id }}";
    // if (!userId) {
    //     // 쿠키 없으면 강제로 1로 설정 (임시) -> 나중에 삭제 
    //     userId = '1';
    //     alert('로그인이 필요합니다. (임시로 user_id=1 사용)');
    // }
    // if (!userId){
    //     userId = '1'
    // }
    const response = await fetch('/modify/search', {
        method : 'POST',
        headers : {'Content-Type': 'application/json'},
        body : JSON.stringify({year, month, day, time})
    })
    const data = await response.json();
    // 조회 페이지 바디 부분 (js로 html 생성)
    const body = document.getElementById('body');
    body.innerHTML= '';
    if (data.length > 0){
        document.getElementById("resultArea").style.display='block';
        const meal = data[0]
        const row = document.createElement("tr");

        row.innerHTML = `
            <td class="d-flex justify-content-between align-items-center">
                <span class="menu-text mb-0">${meal.menu}</span>
                <div>
                    <button type="button" class="btn btn-primary btn-circle btn-sm" onclick="editMeal(${meal.id}, this)">
                        <i class="fas fa-pen"></i>
                    </button>
                    <button type="button" class="btn btn-danger btn-circle btn-sm" onclick="deleteMeal(${meal.id}, this)">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
            `;
        body.appendChild(row);
    }else {
        alert("해당 조건 식단이 존재하지 않습니다.");
    }   
});
// ======================식단 조회 부분 종료======================

// ======================모달 숨김 함수 시작======================
 
function hideModal(modal) {
    document.getElementById('modalOverlay').style.display = 'none'; // 어두운 배경도 꺼야 함
    modal.classList.remove('show'); // Bootstrap 스타일 지우기
    modal.style.display = 'none';
    modal.removeAttribute('aria-modal');
    modal.removeAttribute('role');
}
// ======================모달 숨김 함수 종료======================

// ======================추가 모달 부분 시작======================

// 추가 버튼 클릭 시 모달 생성(보이기) 함수
async function addMeal(){
    document.getElementById('modalOverlay').style.display = 'block'; // 배경 어둡게
    const addModal = document.getElementById('addModal');
    addModal.classList.add('show');
    addModal.style.display = 'block';
    addModal.setAttribute('aria-modal', 'true');
    addModal.setAttribute('role', 'dialog');
    const addInput = document.getElementById('addInput');    
    addInput.focus();
}
// 추가 모달에서 추가 버튼 클릭 시 DB 추가 함수
document.getElementById('add-confirm').onclick = async function () {
    const year = document.getElementById('addYear').value;
    const month = document.getElementById('addMonth').value;
    const day = document.getElementById('addDay').value;
    const time = document.getElementById('addTime').value;
    const newMenu = document.getElementById('addInput').value;
    let userId = "{{ user_id }}"; 
    if (!userId) {
        // 쿠키에 없으면 강제로 1로 설정
        userId = '1';
        alert('로그인이 필요합니다. (임시로 user_id=1 사용)');
    }
    const response = await fetch('/modify/add',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id:userId, year, month, day, time, menu: newMenu})
    })
    //추가 후 페이지 reload
    if (response.ok){
        alert("추가가 완료되었습니다.");
        location.reload();
    }else{
        const result = await response.json();
        alert(result.reason || "추가를 실패하였습니다.");
    }
    //추가 모달 숨김 함수 호출
    hideModal(document.getElementById('addModal'));
}
// 추가 모달에서 취소 버튼 클릭 시 모달 숨김
document.getElementById('add-cancel').onclick = function () {
    hideModal(document.getElementById('addModal'))
}
// 추가 모달에서 X 버튼 클릭 시 모달 숨김
document.getElementById('cancel-add').onclick = function () {
    hideModal(document.getElementById('addModal'))
}
// ======================추가 모달 부분 종료====================== 

// ======================수정 모달 부분 시작======================

// 수정 버튼(식단 메뉴 우측 버튼) 클릭 시 모달 생성(보이기) 함수 
async function editMeal(id, buttonElement) {
    document.getElementById('modalOverlay').style.display = 'block'; 
    
    editingRow = buttonElement.closest('tr');
    const container = buttonElement.closest('td').querySelector('div > div');
    //기존 데이터를 채워넣기
    const menuText = container.querySelector('strong')?.innerText || '';
    const mutedTexts = container.querySelectorAll('.text-muted.small');
    const dateText = mutedTexts[0]?.innerText.trim() || '';
    const timeText = mutedTexts[1]?.innerText.trim() || '';
    // 날짜 파싱
    const dateParts = dateText.match(/\d+/g);
    const [year, month, day] = dateParts || ['', '', ''];

    // 모달에 값 입력
    document.getElementById('editInput').value = menuText;
    document.getElementById('editYear').value = year;
    document.getElementById('editMonth').value = month;
    document.getElementById('editDay').value = day;
    document.getElementById('editTime').value = timeText;


    const editModal = document.getElementById('editModal');
    editModal.classList.add('show');
    editModal.style.display = 'block';
    editModal.setAttribute('aria-modal', 'true');
    editModal.setAttribute('role', 'dialog');
    document.getElementById('editInput').focus();

    editingRow.dataset.id = id; // 수정 대상 ID 저장
}


// 수정 모달에서 수정 버튼 클릭 시 호출 함수 
document.getElementById('edit-confirm').onclick = async function () {
    if (editingRow) {
        const newMenu = document.getElementById('editInput').value.trim();
        if (newMenu !== "") {
            const id = editingRow.dataset.id;
            const year = document.getElementById('editYear').value;
            const month = document.getElementById('editMonth').value;
            const day = document.getElementById('editDay').value;
            const time = document.getElementById('editTime').value;
            const newMenu = document.getElementById('editInput').value;
            const response = await fetch('/modify/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id, year,month,day,time,menu: newMenu})
            });
            if (response.ok){
                alert("수정이 완료되었습니다.");
                const menuSpan = editingRow.querySelector('.menu-text');
                if (menuSpan) {
                    menuSpan.innerText = newMenu;
                } else {
                    console.error('menu-text 클래스를 가진 요소를 찾을 수 없습니다.');
                }
                location.reload();
            }else{
                alert("수정을 실패하였습니다.")
            }
        }
    }
    hideModal(document.getElementById('editModal'));
};

// 수정 취소 (x 버튼, 취소 버튼)
document.getElementById('edit-cancel').onclick = function () {
    hideModal(document.getElementById('editModal'));
};
document.getElementById('cancel-edit').onclick = function () {
    hideModal(document.getElementById('editModal'));
};

// ======================수정 모달 부분 종료====================== 

// ======================삭제 모달 부분 시작====================== 

// 삭제 버튼 클릭 시 모달 생성(보이기) 함수 
async function deleteMeal(id, buttonElement) {
    document.getElementById('modalOverlay').style.display = 'block';
    deletingRow = buttonElement.closest('tr');

    const deleteModal = document.getElementById('deleteModal');
    deleteModal.classList.add('show');
    deleteModal.style.display = 'block';
    deleteModal.setAttribute('aria-modal', 'true');
    deleteModal.setAttribute('role', 'dialog');
    const deleteCancelButton = document.getElementById('delete-cancel');
    if (deleteCancelButton) {
        deleteCancelButton.focus();
    }
    // 삭제 완료 후 삭제 메뉴 id 저장 
    deletingRow.dataset.id = id;
}

// 삭제 모달에서 삭제 버튼 눌렀을 때 
document.getElementById('delete-confirm').onclick = async function () {
    const temp_id = deletingRow.dataset.id
    const response = await fetch('/modify/delete', {
        method: 'POST',
        headers : {'Content-Type':'application/json'},
        body: JSON.stringify({id:temp_id})
    });
    if (response.ok){
        alert("삭제가 완료되었습니다.");
        location.reload();
    }else{
        alert("삭제를 실패하였습니다.")
    }
    hideModal(document.getElementById('deleteModal'));
};

// 삭제 취소 (x 버튼, 취소 버튼 둘 다)
document.getElementById('delete-cancel').onclick = function () {
    hideModal(document.getElementById('deleteModal'))
}
document.getElementById('cancel-delete').onclick = function () {
    hideModal(document.getElementById('deleteModal'))
}
// ======================삭제 모달 부분 종료======================