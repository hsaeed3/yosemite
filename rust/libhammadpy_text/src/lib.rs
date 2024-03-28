use colored::*;
use pyo3::prelude::*;

/// Formats the given text with the specified color, background color, and text styles.
#[pyfunction]
#[pyo3(signature = (message, color = "None", bg = "None", bold = false, italic = false, underline = false))]
fn format_text(message: &str, color: Option<&str>, bg: Option<&str>, bold: bool, italic: bool, underline: bool) -> PyResult<String> {
    let mut styled_message = message.to_string();

    if bold {
        styled_message = styled_message.bold().to_string();
    }
    if italic {
        styled_message = styled_message.italic().to_string();
    }
    if underline {
        styled_message = styled_message.underline().to_string();
    }

    if let Some(color_str) = color {
        styled_message = styled_message.color(parse_color(color_str)).to_string();
    }

    if let Some(bg_color_str) = bg {
        styled_message = styled_message.on_color(parse_color(bg_color_str)).to_string();
    }

    Ok(styled_message)
}

/// Formats a list of items with the specified color, background color, and text styles.
#[pyfunction]
#[pyo3(signature = (items, color = "None", bg = "None", bold = false, italic = false, underline = false))]
fn format_list(items: Vec<String>, color: Option<&str>, bg: Option<&str>, bold: bool, italic: bool, underline: bool) -> PyResult<Vec<String>> {
    let colored_items: Vec<String> = items
        .into_iter()
        .map(|item| {
            let mut styled_item = item.to_string();

            if bold {
                styled_item = styled_item.bold().to_string();
            }
            if italic {
                styled_item = styled_item.italic().to_string();
            }
            if underline {
                styled_item = styled_item.underline().to_string();
            }

            if let Some(color_str) = color {
                styled_item = styled_item.color(parse_color(color_str)).to_string();
            }

            if let Some(bg_color_str) = bg {
                styled_item = styled_item.on_color(parse_color(bg_color_str)).to_string();
            }

            styled_item
        })
        .collect();

    Ok(colored_items)
}

fn parse_color(color: &str) -> Color {
    match color {
        "black" => Color::Black,
        "red" => Color::Red,
        "green" => Color::Green,
        "yellow" => Color::Yellow,
        "blue" => Color::Blue,
        "magenta" | "purple" => Color::Magenta,
        "cyan" => Color::Cyan,
        "white" => Color::White,
        "bright_black" => Color::BrightBlack,
        "bright_red" => Color::BrightRed,
        "bright_green" => Color::BrightGreen,
        "bright_yellow" => Color::BrightYellow,
        "bright_blue" => Color::BrightBlue,
        "bright_magenta" => Color::BrightMagenta,
        "bright_cyan" => Color::BrightCyan,
        "bright_white" => Color::BrightWhite,
        _ => parse_rgb(color),
    }
}

fn parse_rgb(color: &str) -> Color {
    if color.starts_with("rgb(") && color.ends_with(")") {
        let rgb: Vec<&str> = color[4..color.len() - 1].split(',').collect();
        if rgb.len() == 3 {
            let r = rgb[0].trim().parse().unwrap_or(255);
            let g = rgb[1].trim().parse().unwrap_or(255);
            let b = rgb[2].trim().parse().unwrap_or(255);
            Color::TrueColor { r, g, b }
        } else {
            Color::White
        }
    } else {
        Color::White
    }
}

#[pymodule]
fn libhammadpy_text(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(format_text, m)?)?;
    m.add_function(wrap_pyfunction!(format_list, m)?)?;
    Ok(())
}