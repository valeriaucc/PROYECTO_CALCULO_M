// src/views/ColorPicker.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import ColorPicker from "./ColorPicker";

test("1) El color inicial es verde", () => {
  render(<ColorPicker />);
  const box = screen.getByTestId("color-box"); // CORREGIDO
  expect(box).toHaveStyle("background-color: #ffffff");
});

test("2) Cambia el color al seleccionar uno nuevo", () => {
  render(<ColorPicker />);
  const input = screen.getByLabelText(/seleccionar color/i);
  fireEvent.change(input, { target: { value: "#00ff00" } });
  const box = screen.getByTestId("color-box");
  expect(box).toHaveStyle("background-color: #00ff00");
});
