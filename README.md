# Paper Search Service
Search paper's meta information with doi/pmid/arxiv

# 运行

``` bash
poetry install
poetry run python manager runserver
```

# 接口文档
http://127.0.0.1:8000/api/docs


- DOI接口
``` text 
POST http://localhost:8000/api/doi
请求数据 =>  {
                "query": "10.1007/bf02983529"
            }
Content-Type: application/json
```
返回结果
``` json
{
  "code": 2000,
  "result": {
    "origin_url": "http://dx.doi.org/10.1007/bf02983529",
    "title": "Diamond-Blackfan Anemia in Japan: Clinical Outcomes of Prednisolone Therapy and Hematopoietic Stem Cell Transplantation",
    "author": [
      "Shouichi Ohga",
      "Hideo Mugishima",
      "Akira Ohara",
      "Seiji Kojima",
      "Kohji Fujisawa",
      "Keiko Yagi",
      "Masamune Higashigawa",
      "Ichiro Tsukimoto"
    ],
    "organization": [
      "for the Aplastic Anemia Committee of the Japanese Society of Pediatric Hematology"
    ],
    "magazine": [
      "International Journal of Hematology"
    ],
    "publisher": "Springer Science and Business Media LLC",
    "publication_year": 2023,
    "category": [],
    "research_area": null,
    "issue_description": null,
    "pmid": null,
    "doi": "10.1007/bf02983529",
    "arxiv": null,
    "summary": null
  },
  "message": "Success",
  "success": true
}
```

- Pubmed接口
``` text 
POST http://localhost:8000/api/pubmed
请求数据 =>  {
                "query": "31173853"
            }
Content-Type: application/json
```
返回结果
``` json
{
  "code": 2000,
  "result": {
    "origin_url": "http://dx.doi.org/10.1016/j.canlet.2019.05.035",
    "title": "Exosomal transfer of miR-501 confers doxorubicin resistance and tumorigenesis via targeting of BLID in gastric cancer",
    "author": [
      "Xu Liu",
      "Ying Lu",
      "Yunchao Xu",
      "Sizhu Hou",
      "Jinli Huang",
      "Bo Wang",
      "Jinyao Zhao",
      "Shilin Xia",
      "Shujun Fan",
      "Xiaotang Yu",
      "Yue Du",
      "Li Hou",
      "Zhiyue Li",
      "Zijie Ding",
      "Shuo An",
      "Bo Huang",
      "Lianhong Li",
      "Jianwu Tang",
      "Jingfang Ju",
      "Hongwei Guan",
      "Bo Song"
    ],
    "organization": [],
    "magazine": [
      "Cancer Letters"
    ],
    "publisher": "Elsevier BV",
    "publication_year": 2024,
    "category": [],
    "research_area": null,
    "issue_description": null,
    "pmid": null,
    "doi": "10.1016/j.canlet.2019.05.035",
    "arxiv": null,
    "summary": null
  },
  "message": "Success",
  "success": true
}
```

- arXiv接口
``` text 
POST http://localhost:8000/api/arxiv
请求数据 =>  {
                "query": "2008.09595"
            }
Content-Type: application/json
```
返回结果
``` json
{
  "code": 2000,
  "result": {
    "origin_url": "http://arxiv.org/abs/2008.09595v4",
    "title": "Isolated singularities for the n-Liouville equation",
    "author": [
      "Pierpaolo Esposito"
    ],
    "organization": null,
    "magazine": [
      "arXiv"
    ],
    "publisher": "arXiv",
    "publication_year": 2020,
    "category": [
      "Analysis of PDEs",
      "35A21, 35B40 (Primary) 35B33, 35J92 (Secondary)"
    ],
    "research_area": null,
    "issue_description": null,
    "pmid": null,
    "doi": null,
    "arxiv": "2008.09595",
    "summary": "In dimension n isolated singularities -- at a finite point or at infinity --\nfor solutions of finite total mass to the n-Liouville equation are of\nlogarithmic type. As a consequence, we simplify the classification argument in\narXiv:1609.03608 and establish a quantization result for entire solutions of\nthe singular n-Liouville equation."
  },
  "message": "Success",
  "success": true
}
```

