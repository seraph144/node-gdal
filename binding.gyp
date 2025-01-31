{
	"includes": ["common.gypi"],
	"variables": {
		"shared_gdal%": "false",
		"runtime_link%": "shared",
		"enable_logging%": "false"
	},
	"targets": [
		{
			"target_name": "<(module_name)",
			"type": "loadable_module",
			"win_delay_load_hook": "true",
			"product_prefix": "",
			"product_extension": "node",
			"sources": [
				"src/utils/typed_array.cpp",
				"src/utils/string_list.cpp",
				"src/utils/number_list.cpp",
				"src/utils/translate_options.cpp",
				"src/utils/warp_options.cpp",
				"src/utils/ptr_manager.cpp",
				"src/node_gdal.cpp",
				"src/gdal_common.cpp",
				"src/gdal_dataset.cpp",
				"src/gdal_driver.cpp",
				"src/gdal_rasterband.cpp",
				"src/gdal_majorobject.cpp",
				"src/gdal_feature.cpp",
				"src/gdal_feature_defn.cpp",
				"src/gdal_field_defn.cpp",
				"src/gdal_geometry.cpp",
				"src/gdal_point.cpp",
				"src/gdal_linestring.cpp",
				"src/gdal_linearring.cpp",
				"src/gdal_polygon.cpp",
				"src/gdal_geometrycollection.cpp",
				"src/gdal_multipoint.cpp",
				"src/gdal_multilinestring.cpp",
				"src/gdal_multipolygon.cpp",
				"src/gdal_layer.cpp",
				"src/gdal_coordinate_transformation.cpp",
				"src/gdal_spatial_reference.cpp",
				"src/gdal_warper.cpp",
				"src/gdal_algorithms.cpp",
				"src/collections/dataset_bands.cpp",
				"src/collections/dataset_layers.cpp",
				"src/collections/layer_features.cpp",
				"src/collections/layer_fields.cpp",
				"src/collections/feature_fields.cpp",
				"src/collections/feature_defn_fields.cpp",
				"src/collections/geometry_collection_children.cpp",
				"src/collections/polygon_rings.cpp",
				"src/collections/linestring_points.cpp",
				"src/collections/rasterband_overviews.cpp",
				"src/collections/rasterband_pixels.cpp",
				"src/collections/gdal_drivers.cpp"
			],
			"include_dirs": [
				"<!(node -e \"require('nan')\")"
			],
			"defines": [
				"PLATFORM='<(OS)'",
				"_LARGEFILE_SOURCE",
				"_FILE_OFFSET_BITS=64"
			],
			"ldflags": [
				"-Wl,-z,now"
			],
			"xcode_settings": {
				"GCC_ENABLE_CPP_EXCEPTIONS": "YES",
				"OTHER_LDFLAGS":[
					"-Wl,-bind_at_load"
				]
			},
			"conditions": [
				["enable_logging == 'true'", {
					"defines": [
						"ENABLE_LOGGING=1"
					]
				}],
				["shared_gdal == 'false'", {
					"dependencies": [
						"deps/sqlite3/deps/sqlite3.gyp:sqlite3",
						"deps/libgdal/libgdal.gyp:libgdal"
					]
				}, {
					"conditions": [
						['OS == "win"', {
							"libraries": [
								"-lsecur32.lib",
								"-lws2_32.lib",
								"-lodbccp32.lib",
								"-lodbc32.lib"
							],
							"include_dirs": [
								"deps/libgdal/arch/win",
								"deps/libgdal/gdal",
								"deps/libgdal/gdal/alg",
								"deps/libgdal/gdal/apps",
								"deps/libgdal/gdal/gcore",
								"deps/libgdal/gdal/port",
								"deps/libgdal/gdal/bridge",
								"deps/libgdal/gdal/frmts",
								"deps/libgdal/gdal/frmts/zlib",
								"deps/libgdal/gdal/ogr",
								"deps/libgdal/gdal/ogr/ogrsf_frmts",
								"deps/libgdal/gdal/ogr/ogrsf_frmts/mem"
							],
						}, {
							"conditions": [
								["runtime_link == 'static'", {
									"libraries": ["<!@(gdal-config --dep-libs)","<!@(gdal-config --libs)"]
								}, {
									"libraries": ["<!@(gdal-config --libs)"]
								}]
							],
							"cflags_cc": ["<!@(gdal-config --cflags)"],
							"xcode_settings": {
								"OTHER_CPLUSPLUSFLAGS":[
									"<!@(gdal-config --cflags)"
								]
							}
						}]
					]
				}],
				["'<(mrsid_include)' != ''", {
					"conditions": [
						["OS == 'win'", {
							"libraries": [
								"<(mrsid_include)/Raster_DSDK/lib/lti_dsdk.lib",
								"<(mrsid_include)/Raster_DSDK/lib/lti_dsdk_cdll.lib",
								"<(mrsid_include)/Lidar_DSDK/lib/lti_lidar_dsdk.lib"
							]
						}],
						["OS != 'win'", {
							"libraries": [
								"<!@(node -p \"require('fs').readdirSync('<(mrsid_include)/Raster_DSDK/lib/').map(f=>'<(mrsid_include)/Raster_DSDK/lib/'+f).join(' ')\")",
								"<!@(node -p \"require('fs').readdirSync('<(mrsid_include)/Lidar_DSDK/lib/').map(f=>'<(mrsid_include)/Lidar_DSDK/lib/'+f).join(' ')\")"
							]
						}]
					]
				}]
			]
		},
		{
			"target_name": "action_after_build",
			"type": "none",
			"dependencies": [ "<(module_name)" ],
			"copies": [
				{
					"files": [
						"<(PRODUCT_DIR)/<(module_name).node"
					],
					"destination": "<(module_path)"
				}
			],
			"conditions" : [
				["'<(mrsid_include)' != ''", {
					"copies": [
						{
							"files": [
								"<!@(node -p \"require('fs').readdirSync('<(mrsid_include)/Raster_DSDK/lib/').map(f=>'<(mrsid_include)/Raster_DSDK/lib/'+f).join(' ')\")",
								"<!@(node -p \"require('fs').readdirSync('<(mrsid_include)/Lidar_DSDK/lib/').map(f=>'<(mrsid_include)/Lidar_DSDK/lib/'+f).join(' ')\")"
							],
							"destination": "<(module_path)"
						}
					]
				}]
			]
		}
	]
}
