
-- uesrs 테이블에 열 추가하는 query 입니다. 
ALTER TABLE users ADD COLUMN fullname varchar(100) NOT NULL;

-- 이건 users의 컬럼에 해당하는 값을 수정하는 query 입니다 id는 데이터 저장에 따라 바꿔야 합니다..
-- UPDATE users SET name ='kim@naver.com' where id = 1;
-- UPDATE users SET fullname ='kim' where id = 1;

