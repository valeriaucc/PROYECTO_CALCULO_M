// src/views/CountdownTimer.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { act } from "react";
import CountdownTimer from "./CountdownTimer";

jest.useFakeTimers();

test("1) Muestra el tiempo inicial correctamente", () => {
  render(<CountdownTimer />);
  const input = screen.getByLabelText(/segundos/i);
  fireEvent.change(input, { target: { value: "5" } });

  fireEvent.click(screen.getByRole("button", { name: /🚀 iniciar/i }));
  expect(screen.getByText(/5 segundos restantes/i)).toBeInTheDocument();
});

test("2) Disminuye en intervalos de un segundo", () => {
  render(<CountdownTimer />);
  const input = screen.getByLabelText(/segundos/i);
  fireEvent.change(input, { target: { value: "3" } });

  fireEvent.click(screen.getByRole("button", { name: /🚀 iniciar/i }));
  act(() => jest.advanceTimersByTime(1000));
  expect(screen.getByText(/2 segundos restantes/i)).toBeInTheDocument();
});

test("3) Se detiene en 0", () => {
  render(<CountdownTimer />);
  const input = screen.getByLabelText(/segundos/i);
  fireEvent.change(input, { target: { value: "2" } });

  fireEvent.click(screen.getByRole("button", { name: /🚀 iniciar/i }));
  act(() => jest.advanceTimersByTime(3000));
  expect(screen.getByText(/¡tiempo terminado!/i)).toBeInTheDocument();
});
