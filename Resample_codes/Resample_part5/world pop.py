////////////////////////////////////
//world pop
///////////////////////////////////
//导出影像数据函数,三个参数
// 加载WorldPop全球人口数据集合
var worldpop = ee.ImageCollection('WorldPop/GP/100m/pop').select('population');

// 定义全球范围的矩形区域
var globalRegion = ee.Geometry.Rectangle([-180, -90, 180, 90], null, false);

// 导出影像到Google Drive的函数
function exportImage(image, region, fileName) {  
  Export.image.toDrive({  
    image: image,  // 要输出的影像
    description: fileName,  // 下载任务的名称
    fileNamePrefix: fileName,  // 下载影像的文件名前缀
    folder: "WorldPop_Population",  // Drive中存储的文件夹名称
    scale: 11000, // 空间分辨率，单位：米 (约11公里，适合全球尺度)
    region: region,  // 下载影像的范围
    maxPixels: 1e13, // 最大像元数，确保能覆盖全球范围
    fileFormat: "GeoTIFF", // 导出格式
    crs: "EPSG:4326"  // 投影信息，WGS84地理坐标系
  });  
} 

// 获取集合中所有影像的索引（通常是年份信息）
var indexList = worldpop.reduceColumns(ee.Reducer.toList(), ["system:index"]).get("list");  
print("可用的年份列表", indexList);

// 循环导出每一年的影像
indexList.evaluate(function(indexs) {  
  for (var i = 0; i < indexs.length; i++) {  
    // 筛选对应年份的影像
    var image = worldpop.filter(ee.Filter.eq("system:index", indexs[i]))
                        .first()  // 获取该年份的影像
                        .int16(); // 转换为Int16格式，确保导出兼容性
    
    // 导出影像，文件名为"WorldPop_年份"
    exportImage(image, globalRegion, "WorldPop_" + indexs[i]); 
  }  
});