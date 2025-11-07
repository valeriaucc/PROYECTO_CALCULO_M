// src/views/DigitalClock.test.tsx
import { render, screen } from "@testing-library/react";
import { act } from "react"; // CORREGIDO
import DigitalClock from "./DigitalClock";

jest.useFakeTimers();

test("Muestra la hora y se actualiza con el tiempo simulado", () => {
  render(<DigitalClock />);

  const initialTime = screen.getByTestId("clock-time").textContent;

  act(() => {
    jest.advanceTimersByTime(2000); // Avanza el tiempo 2 segundos
  });

  const updatedTime = screen.getByTestId("clock-time").textContent;
  expect(updatedTime).not.toBe(initialTime);
});
