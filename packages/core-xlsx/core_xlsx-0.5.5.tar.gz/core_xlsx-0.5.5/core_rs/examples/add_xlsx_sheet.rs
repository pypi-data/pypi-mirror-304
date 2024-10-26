use std::time::Instant;

use core_rs::types::XLSXSheet;

fn main() -> anyhow::Result<()> {
    let mut sheet = XLSXSheet::new("A".to_string(), 1, 5, 5);

    println!("Добавление 1000x1000 ячеек");

    let start = Instant::now();
    for r in 1..=1000 {
        for c in 1..=1000 {
            sheet.write_cell(r, c, format!("Жопа {};{}", r, c))?;
        }
    }
    let end = start.elapsed();
    println!(
        "Добавлено за: {}.{:03} сек. Кол-во ячеек: {}",
        end.as_secs(),
        end.subsec_millis(),
        sheet.cells.len()
    );

    let mut sheet = XLSXSheet::new("B".to_string(), 1, 5, 5);

    println!("\nДобавление значения в ячейку 100:100");
    let _ = sheet.write_cell(100, 100, "Жопа".to_string());
    let _ = sheet.write_cell_with_formula(99, 99, "Жопа".to_string(), "SUM(A1:A100)".to_string());

    let _ = sheet.write_style_for_cell(100, 100, "StyleID".to_string());

    for cell in sheet.cells.iter() {
        // println!("{} -> {}:{}", cell.cell, cell.row, cell.column);

        if cell.row == 99 && cell.column == 99 {
            println!(
                "{} -> {}:{} __ value: {:?} __ formula: {:?}",
                cell.cell, cell.row, cell.column, cell.value, cell.formula
            );
        }

        if cell.row == 100 && cell.column == 100 {
            println!(
                "{} -> {}:{} __ value: {:?} style_id: {:?}",
                cell.cell, cell.row, cell.column, cell.value, cell.style_id
            );
        }
    }

    println!("max row: {}, max col: {}", sheet.max_row, sheet.max_column);
    println!("cnt {}", sheet.cells.len());

    Ok(())
}
