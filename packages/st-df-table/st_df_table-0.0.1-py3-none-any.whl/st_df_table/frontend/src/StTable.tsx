import React, {useEffect} from "react";
import {Streamlit, withStreamlitConnection} from "streamlit-component-lib";
import BootstrapTable, {ColumnDescription} from 'react-bootstrap-table-next';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';

interface Props {
    args: any;
}

const StTable: React.FC<Props> = (props) => {
    const {args} = props;
    const head_align = args.head_align
    const data_align = args.data_align
    const head_bg_color = args.head_bg_color
    const data_bg_color = args.data_bg_color
    const head_color = args.head_color
    const data_color = args.data_color
    const head_font_weight = args.head_font_weight
    const data_font_weight = args.data_font_weight
    const bordered = args.bordered
    const border_color = args.border_color
    let border_width = args.border_width
    const table_width = args.table_width

    if (!bordered) {
        border_width = 0
    }

    const columns = args.columns.map((col: ColumnDescription) => ({
        ...col,
        headerStyle: {
            textAlign: head_align,
            backgroundColor: head_bg_color,
            color: head_color,
            fontWeight: head_font_weight
        },
        style: {
            textAlign: col.align || data_align,
            backgroundColor: data_bg_color,
            color: data_color,
            fontWeight: data_font_weight
        }
    }));
    const data = args.data;


    useEffect(() => {
        // const tableHeight = Math.min(500, Math.max(data.length * (40 + parseInt(border_width)) + 50, 150));
        // const tableHeight = Math.min(500, Math.max(data.length * (40 + border_width) + 50, 150));
        const tableHeight = data.length * (40 + border_width) + 49
        console.log(border_width)
        console.log(tableHeight)
        Streamlit.setFrameHeight(tableHeight);
    }, [data]);

    return (
        <div style={table_width ? { width: table_width } : {}}>
            <style>{`
                .custom-border.react-bootstrap-table,
                .custom-border.react-bootstrap-table table {
                border: ${border_width}px ${border_color} solid !important;
            }
            .custom-border.react-bootstrap-table th,
            .custom-border.react-bootstrap-table td {
            border: ${border_width}px ${border_color} solid !important;
            }
        `}</style>

            <BootstrapTable keyField='id' data={data} columns={columns}
                            wrapperClasses="custom-border" bordered={bordered}/>
        </div>
    );
};

export default withStreamlitConnection(StTable);
