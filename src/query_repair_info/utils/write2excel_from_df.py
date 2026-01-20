import pandas as pd
import logging

logger = logging.getLogger(__name__)

def write_df_to_excel(df: pd.DataFrame, file_path: str) -> None:
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=0, header=True, index_label=None, freeze_panes=(1,0))
            df_cols = len(df.columns)
            df_rows = len(df)
            col_map = {name: i for i, name in enumerate(df.columns)}
                        
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']
            
            format_number = workbook.add_format({
                'num_format': '0',
                'font_name': 'Yu Gothic',
                'border': 1
                })
            
            format_datetime = workbook.add_format({
                'num_format': 'yyyy/mm/dd hh:mm:ss',
                'font_name': 'Yu Gothic',
                'border': 1
                })
            
            format_text = workbook.add_format({
                'font_name': 'Yu Gothic',
                'border': 1
                })
            
            format_center = workbook.add_format({
                'font_name': 'Yu Gothic',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
                })
            
            highlight_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'font_color': '#9C0006'
            })
            
            worksheet.set_column(col_map['修理前IMEI'], col_map['修理後IMEI'], 18, format_number)
            worksheet.set_column(col_map['管理番号'], col_map['管理番号'], 14, format_text)
            worksheet.set_column(col_map['修理報告時間'], col_map['修理報告時間'], 20, format_datetime)
            worksheet.set_column(col_map['修理パターン'], col_map['責任'], 14, format_text)
            worksheet.set_column(col_map['責任'] + 1, col_map['その他'] - 1, 10, format_center)
            worksheet.set_column(col_map['その他'], col_map['その他'], 10, format_text)
            # worksheet.set_column(0, 1, 18, format_number)
            # worksheet.set_column(2, 2, 20, format_datetime)
            # worksheet.set_column(3, 6, 14, format_text)
            # worksheet.set_column(7, df_cols-2, 10, format_center)
            # worksheet.set_column(df_cols-1, df_cols-1, 10, format_text)
            
            # 高亮显示重复维修前IMEI
            worksheet.conditional_format(f'A1:A{df_rows}', {
                'type': 'formula',
                'criteria': f'=COUNTIF($A$1:$A${df_rows}, A1)>1',
                'format': highlight_format
            })
            
            logger.info(f"DataFrame successfully written to {file_path}")

    except Exception as e:
        logger.error(f"Failed to write DataFrame to Excel: {e}")
        raise SystemExit(1)