def get_all_capsules(conn):
    """활성화된 캡슐만 가져오기"""
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM capsules WHERE is_active = 1 ORDER BY name ASC"
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"조회 에러: {e}")
        return []

# 테이블 생성 함수
def create_tables(conn):
    if conn is None:
        print("DB 연결이 유효하지 않습니다.")
        return

    with conn.cursor() as cursor:
        # 캡슐 마스터 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS capsules (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                brand VARCHAR(30) DEFAULT 'illy',
                intensity INT,
                acidity INT,
                stock_count INT DEFAULT 0
            )
        """)
        
        # 소비 기록 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumption_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                capsule_id INT,
                drink_type VARCHAR(20),
                consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (capsule_id) REFERENCES capsules(id)
            )
        """)
    conn.commit()
    print("테이블이 성공적으로 생성되었습니다.")


# 캡슐 소비 함수
def consume_capsule(conn, capsule_id, drink_type="아이스 아메리카노"):
    """캡슐을 하나 마셨을 때 로그를 남기고 재고를 줄입니다."""
    try:
        with conn.cursor() as cursor:
            # 소비 로그 추가
            sql_log = "INSERT INTO consumption_log (capsule_id, drink_type) VALUES (%s, %s)"
            cursor.execute(sql_log, (capsule_id, drink_type))
            
            # 재고 차감 (-1)
            sql_update = "UPDATE capsules SET stock_count = stock_count - 1 WHERE id = %s"
            cursor.execute(sql_update, (capsule_id,))
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return False

# 다 먹은 캡슐 숨기기
def hide_capsule(conn, capsule_id):
    """캡슐을 삭제하지 않고 숨김 처리"""
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE capsules SET is_active = 0 WHERE id = %s"
            cursor.execute(sql, (capsule_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"숨기기 에러: {e}")
        return False

# 캡슐 신규 등록 함수
def add_capsule(conn, name, brand, intensity, acidity, stock):
    try:
        with conn.cursor() as cursor:
            # 이름(name)이 같으면 stock_count만 기존 값에 더해주는 쿼리
            sql = """
                INSERT INTO capsules (name, brand, intensity, acidity, stock_count)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                stock_count = stock_count + VALUES(stock_count)
            """
            cursor.execute(sql, (name, brand, intensity, acidity, stock))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False        


# 날짜별 소비량
def get_consumption_by_date(conn):
    """날짜별 커피 소비량을 가져옵니다."""
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT DATE(consumed_at) as date, COUNT(*) as count 
                FROM consumption_log 
                GROUP BY DATE(consumed_at)
                ORDER BY date ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"조회 에러: {e}")
        return []        