-- 0. 기존 test 데이터베이스 삭제 (있을 경우)
DROP DATABASE IF EXISTS test;

-- 1. 데이터베이스 생성
CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 해당 데이터베이스 사용
USE test;

-- 3. users 테이블 생성
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3-1. users 테이블에 fullname 열 추가
ALTER TABLE users ADD COLUMN fullname VARCHAR(100) NOT NULL;

-- 4. users 더미 데이터 삽입
INSERT INTO users (id, name, password, fullname) VALUES
(1, 'kim@naver.com', '1234', 'Kim Minsoo'),
(2, 'Lee@naver.com', '1234', 'Lee Jieun');

-- 5. users 테이블 조회
SELECT * FROM users;

-- 6. diets 테이블 생성
CREATE TABLE diets (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT DEFAULT NULL,
  menu VARCHAR(100) DEFAULT NULL,
  date DATE NOT NULL,
  time VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  KEY user_id (user_id),
  CONSTRAINT diets_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 7. diets 더미 데이터 삽입
INSERT INTO diets (id, user_id, menu, date, time) VALUES
(2, 1, '햄버거', '2025-01-01', '아침'),
(3, 1, '피자', '2025-01-01', '점심'),
(4, 1, '치킨', '2025-01-01', '저녁'),
(5, 1, '밥, 미역국', '2025-01-02', '아침'),
(6, 1, '밥, 김치, 참치', '2025-01-02', '점심'),
(7, 1, '샌드위치, 우유', '2025-01-02', '저녁');

-- 8. diets 테이블 조회
SELECT * FROM diets;
SELECT * FROM users;
