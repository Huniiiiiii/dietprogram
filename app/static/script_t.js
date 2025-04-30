//년 월 일 식사시간 선택하고 url 요청
document.getElementById("searchForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const year = document.getElementById("year").value;
    const month = document.getElementById("month").value;
    const day = document.getElementById("day").value;

    const time = document.getElementById('time').value;
    const response = await fetch('/modify/search', {
        method :'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({year,month, day, time})
    })

    const data = await response.json();
    const body = document.getElementById('body');
    body.innerHTML= '';
    if (data.length > 0){
        document.getElementById("resultArea").style.display='block';
        const row = document.createElement("tr");
        const meal = data[0]
        row.innerHTML = `
            <td><p>${meal.menu}</p></td>
            <td><button onclick="updateMeal(${meal.id}, this)">수정</td>
            <td><button onclick="deleteMeal(${meal.id}, this)">삭제</td>
            `;
            body.appendChild(row);
    }else {
        alert("해당 조건 식단이 존재하지 않습니다.");
    }   

});
//메뉴 수정 및 삭제에  필요한 전역 변수 
let newP = null; //기존 메뉴를 대체할 메뉴 
let tempId = null; //조회한 메뉴 

//수정 버튼 클릭 이벤트에 대한 함수 - 모달 생성  
async function updateMeal(id,btn){
    tempId = id;
    newP = btn.closest('tr').querySelector('p');
    document.getElementById('editInput').value = newP.textContent;

    document.getElementById('editModal').style.display = "flex";
    document.getElementById('editModal').focus();
}
//모달에서 수정 버튼 누르는 이벤트에 대한 스크립트 - DB 데이터 변경 
document.getElementById('edit-confirm').addEventListener('click', async () => {
    const newMenu = document.getElementById('editInput').value;

    const response = await fetch('/modify/update', {
        method: 'Post',
        headers: {'Content-Type': 'application/json' },
        body: JSON.stringify({id:tempId, menu : newMenu})
    });
    if (response.ok){
        newP.textContent = newMenu;
        alert('수정이 완료되었습니다.');
    }else{
        alert("수정에 실패하였습니다.");
    }
    document.getElementById('editModal').style.display = 'none';
});
//모달에서 취소 버튼 누르는 이벤트에 대한 스크립트 - 모달 닫기 
document.getElementById('edit-cancel').addEventListener('click', () =>{
    document.getElementById('editModal').style.display = 'none';
});

//삭제 버튼 클릭 이벤트에 대한 함수 - 모달 생성 
async function deleteMeal(id,btn) {
    tempId = id;
    document.getElementById('deleteModal').style.display = "flex";
    document.getElementById('deleteModal').focus();
}

//모달에서 삭제 버튼 누르는 이벤트에 대한 스크립트 - DB 데이터 삭제
document.getElementById('delete-confirm').addEventListener('click', async () => {
    const response = await fetch('/modify/delete', {
        method: 'Post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id:tempId})
    });
    if (response.ok){
        alert("삭제가 완료되었습니다.");
        location.reload();
    }else{
        alert("삭제를 실패하였습니다.");
    }
    document.getElementById('deleteModal').style.display = 'none';  
});
//모달에서 취소 버튼 누르는 이벤트에 대한 스크립트 - 모달 닫기 
document.getElementById('delete-cancel').addEventListener('click', () =>{
    document.getElementById('deleteModal').style.display = 'none';
});