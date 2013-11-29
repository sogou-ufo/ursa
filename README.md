#Ursa

##Description

sogou 前端开发框架

##changelog
 - 同时支持_data/*.json和manifest.json中的多行/**/注释
 - 避免了对url(about:blank)和url(data:image...)加时间戳,但url内部不能用引号
 - 定义require_js_modules数组可定义多个css编译实体
 - 定义html_force_output可避免个别模板出错导致剩余模板不参加编译