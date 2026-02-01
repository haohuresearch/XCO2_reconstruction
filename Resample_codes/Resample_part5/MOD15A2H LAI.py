////////////////////////////////////////////////////////////////////
//MOD15A2H LAI 
////////////////////////////////////////////////////////////////////
//final version
// 定义研究区域（全球范围）
var region = ee.Geometry.Rectangle([-180, -90, 180, 90], null, false);

// 定义数据集 - MODIS LAI数据
var dataset = ee.ImageCollection('MODIS/061/MOD15A2H');

// 定义年份范围
var startYear = 2019;
var endYear = 2025;  // 如果需要到当前年份，可以改为new Date().getFullYear()

// 循环处理每一年
for (var year = startYear; year <= endYear; year++) {
  // 确定每年的开始和结束日期
  var startDate, endDate;
  
  if (year === endYear) {
    // 最后一年只到6月26日（可根据需要调整）
    startDate = year + '-01-01';
    endDate = year + '-06-30';
  } else {
    // 其他年份全年
    startDate = year + '-01-01';
    endDate = year + '-12-31';
  }
  
  // 筛选该年份的数据并按时间排序
  var yearlyData = dataset
    .filter(ee.Filter.date(startDate, endDate))
    .select('Lai_500m')  // 选择LAI波段
    .sort('system:time_start');
  
  // 获取该年份影像的数量
  var count = yearlyData.size().getInfo();
  print('Year ' + year + ' LAI image count: ', count);
  
  // 如果没有数据则跳过该年
  if (count === 0) {
    print('No data for year ' + year + ', skipping...');
    continue;
  }
  
  // 转换为列表以便处理
  var imageList = yearlyData.toList(count);
  
  // 存储处理后的LAI影像列表
  var laiImages = [];
  var dates = [];
  
  // 循环处理每一幅影像，提取LAI并添加日期标识
  for (var i = 0; i < count; i++) {
    var image = ee.Image(imageList.get(i));
    // 获取日期并格式化为字符串
    var date = ee.Date(image.get('system:time_start')).format('yyyyMMdd').getInfo();
    dates.push(date);
    
    // 提取LAI并应用比例因子（根据MOD15A2H数据说明，比例因子为0.1）
    var lai = image.select('Lai_500m').multiply(0.1).rename('LAI_' + date);
    laiImages.push(lai);
  }
  
  // 合并一年中所有LAI影像为一个多层影像（每年一个文件）
  var yearlyLAI = ee.ImageCollection(laiImages).toBands();
  
  // 导出年度LAI（一个文件包含全年所有8天合成数据）
  Export.image.toDrive({
    image: yearlyLAI,
    description: 'MODIS_LAI_' + year,
    folder: 'MODIS_LAI_Yearly',  // 请确保该文件夹已存在
    scale: 11000,  // 设置为11000米分辨率
    region: region,
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
}