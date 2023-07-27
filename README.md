# boss直聘爬虫
## mysql建表语句
CREATE TABLE `boss` (
  `job_name` varchar(1000) DEFAULT NULL COMMENT '工作名称',
  `job_education` varchar(1000) DEFAULT NULL COMMENT '教育经历',
  `job_salary` varchar(1000) DEFAULT NULL COMMENT '薪资待遇',
  `job_skill` varchar(1000) DEFAULT NULL COMMENT '工作技能要求',
  `job_welfare` varchar(1000) DEFAULT NULL COMMENT '公司福利',
  `job_years` varchar(1000) DEFAULT NULL COMMENT '工作年限',
  `company_description` text DEFAULT NULL COMMENT '公司介绍',
  `Job_description` text DEFAULT NULL COMMENT '工作职责',
  `company_name` varchar(1000) DEFAULT NULL COMMENT '公司名称',
  `trade_name` varchar(1000) DEFAULT NULL COMMENT '行业',
  `company_scale` varchar(1000) DEFAULT NULL COMMENT '公司规模',
  `job_url` varchar(1000) DEFAULT NULL COMMENT '网页地址'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci；

