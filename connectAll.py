


# -------------------------------
# KẾT NỐI NEO4J
# -------------------------------



# -------------------------------
# KẾT NỐI MONGODB
# -------------------------------



# -------------------------------
# KẾT NỐI POSTGRESQL
# -------------------------------



# -------------------------------
# KẾT NỐI MINIO – LẤY OBJECT (HÌNH ẢNH)
# -------------------------------



# -------------------------------
# CHẠY THỬ HỆ THỐNG
# -------------------------------
if __name__ == "__main__":
    # ===== Neo4j =====
    neo4j_driver = connect_neo4j()
    result_neo = query_neo4j(neo4j_driver, "MATCH (s:Student) RETURN s LIMIT 5")
    print("Neo4j:", result_neo)

    # ===== MongoDB =====
    mongo_col = connect_mongo()
    result_mongo = query_mongodb(mongo_col, {"class": "4D"})
    print("MongoDB:", result_mongo)

    # ===== PostgreSQL =====
    pg_conn = connect_postgre()
    result_pg = query_postgre(pg_conn, "SELECT id, full_name FROM students LIMIT 5;")
    print("PostgreSQL:", result_pg)

    # ===== MinIO: Lấy ảnh =====
    minio_client = connect_minio()
    bucket_name = "img"
    object_name = "0001001.jpg"
    save_path = "./downloaded_profile.jpg"

    download_image_minio(minio_client, bucket_name, object_name, save_path)

    print("Hoàn tất kết nối và lấy dữ liệu!")
