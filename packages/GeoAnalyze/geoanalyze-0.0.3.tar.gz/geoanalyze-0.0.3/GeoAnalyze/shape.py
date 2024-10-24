import geopandas
import shapely
from .core import Core


class Shape:
    
    '''
    Provides functionality for shapefile operations.
    '''
    
    def columns_retain(
        self,
        input_file: str,
        retain_cols: list[str],
        output_file: str
    )-> geopandas.GeoDataFrame:
        
        '''
        Return a GeoDataFrame with geometry and specified columns. 
        Useful when the user wants to remove unnecessary columns
        while retaining a few required ones.
        
        Parameters
        ----------
        input_file : str 
            Path to the input shapefile.
            
        retain_cols : list 
            List of columns, apart from 'geometry', to include in the output shapefile.

        output_file : str  
            Shapefile path to save the output GeoDataFrame.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame containing the speificed columns.
        '''
        
        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)
        
        # list of columns to drop
        retain_cols = retain_cols + ['geometry']
        drop_cols = [col for col in gdf.columns if col not in retain_cols]
        gdf = gdf.drop(columns=drop_cols)
        
        # saving output GeoDataFrame
        gdf.to_file(output_file)
        
        return gdf
    
    def columns_delete(
        self,
        input_file: str,
        delete_cols: list[str],
        output_file: str
    )-> geopandas.GeoDataFrame:

        '''
        Delete specified columns from a GeoDataFrame. 
        Useful when the user wants to delete specific columns.

        Parameters
        ----------
        input_file : str 
            Path to the input shapefile.

        delete_cols : list 
            List of columns, apart from 'geometry', to delete in the output shapefile.

        output_file : str  
            Shapefile path to save the output GeoDataFrame.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame with trhe deletion of speificed columns.
        '''

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)

        # list of columns to drop
        delete_cols.remove('geometry') if 'geometry' in delete_cols else delete_cols
        gdf = gdf.drop(columns=delete_cols)

        # saving output GeoDataFrame
        gdf.to_file(output_file)

        return gdf
    
    def adding_id_column(
        self,
        input_file: str, 
        column_name: str, 
        output_file: str
    ) -> geopandas.GeoDataFrame:

        '''
        Adds an ID column to the geometries,
        starting from 1 and incrementing by 1.

        Parameters
        ----------
        input_file : str 
            Path to the input shapefile

        colums_name : str 
            Name of the ID column to be added.

        output_file : str 
            Shapefile path to save the output GeoDataFrame.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame with an added ID column,
            where values start from 1 and increase by 1.
        '''

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)

        # insert ID column
        gdf.insert(0, column_name, list(range(1, gdf.shape[0] + 1)))

        # saving output GeoDataFrame
        gdf.to_file(output_file)

        return gdf
    
    def fill_polygon_holes_after_explode(
        self, 
        input_file: str, 
        output_file: str
    ) -> geopandas.GeoDataFrame:
    
        '''
        Explode the multipolygons, if any, into single pieces
        and fill the holes, if any, inside the polygons.
        
        Parameters
        ----------
        input_file : str 
            Path to the input shapefile.

        output_file : str  
            Shapefile path to save the output GeoDataFrame.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame that splits multi-polygons into single pieces
            and filled the holes, if any, inside the polygons.
        '''
        
        # confirming input geometry type is Polygon
        geometry_type = Core().shapefile_geometry_type(
            file_path=input_file
        )
        if 'Polygon' in geometry_type:
            pass
        else:
            raise Exception('Input geometry must be Polygon type.')

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)
        
        # polygon filling
        gdf = gdf.explode(index_parts=False, ignore_index=True)
        gdf = gdf.drop_duplicates(
            subset=['geometry'],
            ignore_index=True
        )
        gdf.geometry = gdf.geometry.apply(
            lambda x: shapely.Polygon(x.exterior.coords)
        )
        
        # saving output geodataframe
        gdf.to_file(output_file)

        return gdf
    
    def fill_polygon_holes(
        self, 
        input_file: str, 
        output_file: str
    ) -> geopandas.GeoDataFrame:
    
        '''
        Fills holes in polygon without exploding into multi-part geometries.
        
        Parameters
        ----------
        input_file : str 
            Path to the input shapefile.

        output_file : str  
            Shapefile path to save the output GeoDataFrame.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame with any holes in the polygons filled.
        '''
        
        # confirming input geometry type is Polygon
        geometry_type = Core().shapefile_geometry_type(
            file_path=input_file
        )
        if 'Polygon' in geometry_type:
            pass
        else:
            raise Exception('Input geometry must be Polygon type.')

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)
        
        # polygon filling
        tmp_col = Core()._tmp_df_column_name(list(gdf.columns))
        gdf = gdf.reset_index(names=[tmp_col])
        gdf = gdf.explode(index_parts=False, ignore_index=True)
        gdf = gdf.drop_duplicates(
            subset=['geometry'],
            ignore_index=True
        )
        gdf.geometry = gdf.geometry.apply(
            lambda x: shapely.Polygon(x.exterior.coords)
        )
        gdf = gdf.dissolve(by=[tmp_col]).reset_index(drop=True)
        
        # saving output geodataframe
        gdf.to_file(output_file)

        return gdf
    
    def extract_intersecting_geometries(
        self, 
        input_file: str, 
        overlay_file: str, 
        output_file: str
    ) -> geopandas.GeoDataFrame:
    
        '''
        Performs a spatial join to extract geometries
        that intersect with other geometries.
        
        Parameters
        ----------
        input_file : str 
            Path to the input shapefile containing the main geometries
            from which extraction will be done.

        overlay_file : str 
            Path to the input shapefile containing intersecting geometries.

        output_file : str 
            Shapefile path to save the output GeoDataFrame of extracted geometries.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame of extracted geometries that intersect with other geometries.
        '''

        # input GeoDataFrame
        input_gdf = geopandas.read_file(input_file)

        # overlay GeoDataFrame
        overlay_gdf = geopandas.read_file(overlay_file)

        # extracting geometries 
        extract_gdf = geopandas.sjoin(
            left_df=input_gdf,
            right_df=overlay_gdf,
            how='inner'
        )
        extract_gdf = extract_gdf.iloc[:, :input_gdf.shape[1]]
        extract_gdf.columns = input_gdf.columns
        extract_gdf = extract_gdf.drop_duplicates(
            subset=['geometry'],
            ignore_index=True
        )
        
        # saving output GeoDataFrame
        extract_gdf.to_file(output_file)

        return extract_gdf
    
    def polygons_area_cumsum_count(
        self,
        shape_file: str
    ) -> dict[float, int]:
        
        '''
        Sorts the polygons by area in descending order and returns a dictionary of
        cumulative percentage areas and the difference in counts between consecutive cumulative areas.

        Parameters
        ----------
        shape_file : str 
            Shapefile path of the input polygons.

        Returns
        -------
        dict
            A dictionary where the keys are cumulative percentage areas of polygons,
            and the values represent the difference in counts between consecutive cumulative areas.
        '''

        # confirming input geometry type is Polygon
        geometry_type = Core().shapefile_geometry_type(
            file_path=shape_file
        )
        if 'Polygon' in geometry_type:
            pass
        else:
            raise Exception('Input geometry must be Polygon type.')

        # input GeoDataFrame
        gdf = geopandas.read_file(shape_file)

        # cumulative area percentage of polygons
        tmp_col = Core()._tmp_df_column_name(list(gdf.columns))
        per_col = tmp_col + '(%)'
        cumsum_col = per_col + '-cs'
        gdf[tmp_col] = gdf.geometry.area
        gdf = gdf.sort_values(by=[tmp_col], ascending=[False])
        gdf[per_col] = 100 * gdf[tmp_col] / gdf[tmp_col].sum()
        gdf[cumsum_col] = gdf[per_col].cumsum().round()
        
        # count cumulative percentage
        cumsum_df = gdf[cumsum_col].value_counts().to_frame().reset_index(names=['Cumsum(%)'])
        cumsum_df = cumsum_df.sort_values(by=['Cumsum(%)'], ascending=[True]).reset_index(drop=True)
        output = dict(
            zip(
                cumsum_df['Cumsum(%)'], 
                cumsum_df['count']
            )
        )

        return output
    
    def remove_polygons_by_area_cumsum_percent(
        self,
        input_file: str,
        percent_cutoff: float,
        output_file: str,
        index_sort: bool = False
    ) -> geopandas.GeoDataFrame:

        '''
        sorts the percentage area of polygons in descending order
        and removes polygons whose cumulative percentage 
        exceeds the specified cutoff (ranging from 0 to 100).

        Parameters
        ----------
        input_file : str 
            Path to the input shapefile.

        percent_cutoff : float 
            Only polygons with a cumulative area percentage less than or equal
            to the specified cutoff (between 0 and 100) are retained.

        output_file : str 
            Shapefile path to save the output GeoDataFrame.
            
        index_sort : bool, False 
            If True, polygons are sorted by their index before sorting cumulative area percentages.

        Returns
        -------
        GeoDataFrame
            A GeoDataFrame containing polygons with a cumulative area percentage
            less than or equal to the specified cutoff.
        '''

        # confirming input geometry type is Polygon
        geometry_type = Core().shapefile_geometry_type(
            file_path=input_file
        )
        if 'Polygon' in geometry_type:
            pass
        else:
            raise Exception('Input geometry must be Polygon type.')

        # input GeoDataFrame
        gdf = geopandas.read_file(input_file)

        # removing polygons
        tmp_col = Core()._tmp_df_column_name(list(gdf.columns))
        per_col = tmp_col + '(%)'
        cumsum_col = per_col + '-cs'
        gdf[tmp_col] = gdf.geometry.area
        gdf = gdf.sort_values(by=[tmp_col], ascending=[False])
        gdf[per_col] = 100 * gdf[tmp_col] / gdf[tmp_col].sum()
        gdf[cumsum_col] = gdf[per_col].cumsum()
        gdf = gdf[gdf[cumsum_col] <= percent_cutoff]
        gdf = gdf.sort_index() if index_sort is True else gdf
        gdf = gdf.reset_index(drop=True)
        gdf = gdf.drop(columns=[tmp_col, per_col, cumsum_col])

        # saving output GeoDataFrame
        gdf.to_file(output_file)

        return gdf
    
    
