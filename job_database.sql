
-- DROP DATABASE IF EXISTS MyJob;
-- 创建数据库 MyJob并设置默认字符编码
CREATE DATABASE IF NOT EXISTS MyJob DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

-- 创建数据表
-- DROP TABLE IF EXITST Job;
CREATE TABLE IF NOT EXISTS Job (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT '自增序号',
    job_id NVARCHAR(30) NOT NULL COMMENT '主键',
    job_detail_id NVARCHAR(30) NOT NULL COMMENT 'Job Detail主键',
    job_name NVARCHAR(50) NOT NULL COMMENT '职位名称',
    job_url NVARCHAR(100) NOT NULL COMMENT '职位url',
    job_salary NVARCHAR(20) COMMENT '职位月薪',
    salary_min INT COMMENT '职位月薪Min',
    salary_max INT COMMENT '职位月薪Max',
    job_location NVARCHAR(100) COMMENT '工作地址',
    job_date NVARCHAR(30) COMMENT '职位发布时间',
    company_name NVARCHAR(100) NOT NULL COMMENT '公司名称',
    company_url NVARCHAR(100) COMMENT '公司网址',
    review_percent NVARCHAR(10) COMMENT '反馈率',
    from_app NVARCHAR(10) COMMENT '职位来源',
    create_time DATETIME COMMENT '爬取时间',
    PRIMARY KEY(job_id),
    KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='Job主表';

-- DROP TABLE IF EXITST JobDetail;
CREATE TABLE IF NOT EXISTS JobDetail (
    id INT(10) NOT NULL AUTO_INCREMENT COMMENT '自增序号',
    job_id NVARCHAR(30) NOT NULL COMMENT '主键',
    job_name NVARCHAR(50) NOT NULL COMMENT '职位名称',
    job_url NVARCHAR(100) NOT NULL COMMENT '职位网址',
    job_tags NVARCHAR(200) NOT NULL COMMENT 'tags',
    job_salary NVARCHAR(20) COMMENT '职位月薪',
    salary_min INT COMMENT '职位月薪Min',
    salary_max INT COMMENT '职位月薪Max',
    job_location NVARCHAR(100) COMMENT '工作地址',
    job_date NVARCHAR(30) COMMENT '职位发布时间',
    job_nature NVARCHAR(30) COMMENT '工作性质',
    work_years NVARCHAR(10) COMMENT '工作年限',
    work_years_min INT COMMENT '工作年限Min',
    work_years_max INT COMMENT '工作年限Max',
    min_degree NVARCHAR(20) COMMENT '最低学历要求',
    ofer_members INT COMMENT '招聘人数',
    job_cate NVARCHAR(50) COMMENT '职位类别',
    job_skills TEXT COMMENT '职位要求',
    company_name NVARCHAR(100) NOT NULL COMMENT '公司名称',
    company_url NVARCHAR(100) COMMENT '公司网址',
    company_nature NVARCHAR(50) NOT NULL COMMENT '公司性质',
    company_size NVARCHAR(50) NOT NULL COMMENT '公司性质',
    company_size_min NVARCHAR(50) NOT NULL COMMENT '公司规模Min',
    company_size_max NVARCHAR(50) NOT NULL COMMENT '公司规模Max',
    company_industry NVARCHAR(50) NOT NULL COMMENT '公司行业',
    company_address NVARCHAR(200) NOT NULL COMMENT '公司地址',
    company_intro TEXT NOT NULL COMMENT '公司简介',
    from_app NVARCHAR(10) COMMENT '职位来源',
    PRIMARY KEY(job_id),
    KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='Job祥表';

-- 创建索引
CREATE UNIQUE INDEX index_job_id USING BTREE ON Job (job_id);
CREATE UNIQUE INDEX index_job_detail_id USING BTREE ON Job (job_detail_id);
CREATE UNIQUE INDEX index_job_id USING BTREE ON JobDetail (job_id);
