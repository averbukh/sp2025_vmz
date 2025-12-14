import numpy as np
import io
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path


def validate_params(w: int, d: int) -> None:
    if not isinstance(w, int) or w <= 0 or (w % 4 != 0):
        raise ValueError("w должно быть положительным целым числом, кратным 4.")
    if not isinstance(d, int) or d <= 0:
        raise ValueError("d должно быть положительным целым числом (> 0).")


def load_grayscale_image(image_path: str) -> tuple[Image.Image, np.ndarray]:
    """Открыть изображение и вернуть (PIL_image_grayscale, numpy_array_uint8)."""
    img = Image.open(image_path).convert("L")  # яркость 0..255
    arr = np.array(img, dtype=np.uint8)
    return img, arr


def compute_mu1_signal(img_arr: np.ndarray, w: int, d: int) -> tuple[list[float], list[int]]:
    validate_params(w, d)

    height, width = img_arr.shape
    if w > width:
        raise ValueError(f"w={w} больше ширины изображения ({width}).")

    half = w // 2
    x_vals: list[float] = []
    y_vals: list[int] = []

    # left = 0, d, 2d, ... пока окно [left, left+w) помещается в изображение
    for left in range(0, width - w + 1, d):
        right = left + w
        window = img_arr[:, left:right]              # (H, w)
        left_half = window[:, :half]                # (H, w/2)
        right_half = window[:, half:]               # (H, w/2)

        sum_left = int(np.sum(left_half, dtype=np.int64))
        sum_right = int(np.sum(right_half, dtype=np.int64))

        y = sum_right - sum_left
        x = left + w / 2.0

        x_vals.append(x)
        y_vals.append(y)

    return x_vals, y_vals


def show_table(x: list[float], y: list[int], max_rows: int = 20) -> None:
    """
    Отображение таблицы значений x и y(x).
    """
    df = pd.DataFrame({"x": x, "y(x)=μ1(x)": y})
    print("\nТаблица значений x и y(x):")
    if len(df) <= max_rows:
        print(df.to_string(index=False))
    else:
        head = df.head(max_rows // 2)
        tail = df.tail(max_rows // 2)
        print(head.to_string(index=False))
        print("   ...")
        print(tail.to_string(index=False))


def plot_image_and_signal(image_path: str, x: list[float], y: list[int], w: int, d: int) -> None:
    """
    Отображение исходного изображения и графика y(x),
    а также сохранение графика в форматах SVG и BMP.
    """
    image_name = Path(image_path).stem
    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)

    fig, (ax_img, ax_plot) = plt.subplots(2, 1, figsize=(14, 9))

    img = Image.open(image_path)
    ax_img.imshow(img, cmap="gray")
    ax_img.set_title(f"Исходное изображение: {Path(image_path).name}")
    ax_img.axis("off")

    ax_plot.plot(x, y, linewidth=2, label="y(x)=μ₁(x)")
    ax_plot.axhline(0, linewidth=1)
    ax_plot.set_xlabel("x — координата центра фильтра (пиксели)")
    ax_plot.set_ylabel("y(x) — разность яркостей (правая − левая)")
    ax_plot.set_title(f"F1: y(x)=μ₁(x), w={w}, d={d}")
    ax_plot.grid(True, alpha=0.3)
    ax_plot.legend()

    plt.tight_layout()

    svg_path = output_dir / f"{image_name}_w{w}_d{d}.svg"
    bmp_path = output_dir / f"{image_name}_w{w}_d{d}.bmp"

    
    fig.savefig(svg_path, format="svg")

    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    pil_img = Image.open(buf).convert("RGB")
    pil_img.save(bmp_path, format="BMP")
    buf.close()

    print("Графики сохранены:")
    print(f"  {svg_path}")
    print(f"  {bmp_path}")

    plt.show()
    plt.close(fig)


def process_one_image(image_path: str, w: int, d: int) -> None:
    _, arr = load_grayscale_image(image_path)
    x, y = compute_mu1_signal(arr, w=w, d=d)
    show_table(x, y)
    plot_image_and_signal(image_path, x, y, w=w, d=d)


def main() -> None:
    images = ["01.png", "12.png"]

    print("Изображения:", ", ".join(images))

    while True:
        try:
            w = int(input("\nВведите ширину фильтра w (положительное, кратно 4): ").strip())
            d = int(input("Введите шаг сдвига d (целое > 0): ").strip())
            validate_params(w, d)
        except Exception as e:
            print(f"Ошибка ввода параметров: {e}")
            continue

        for p in images:
            try:
                print(f"\n=== Обработка изображения: {p} ===")
                process_one_image(p, w=w, d=d)
            except Exception as e:
                print(f"Не удалось обработать {p}: {e}")

        again = input("\nПопробовать другие w и d? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()