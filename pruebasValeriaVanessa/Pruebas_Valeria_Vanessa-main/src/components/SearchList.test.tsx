// src/views/SearchList.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import SearchList from "./SearchList";

test("1) Muestra la lista inicial con todos los elementos", () => {
  render(<SearchList />);
  expect(screen.getByText(/ana/i)).toBeInTheDocument();
  expect(screen.getByText(/pedro/i)).toBeInTheDocument();
  expect(screen.getByText(/maría/i)).toBeInTheDocument();
});

test("2) Filtra los nombres al escribir en el input", () => {
  render(<SearchList />);
  const input = screen.getByPlaceholderText(/escribe un nombre/i); // CORREGIDO
  fireEvent.change(input, { target: { value: "Pedro" } });
  expect(screen.getByText(/pedro/i)).toBeInTheDocument();
  expect(screen.queryByText(/ana/i)).not.toBeInTheDocument();
});

test("3) Muestra 'No encontrado' si no hay coincidencias", () => {
  render(<SearchList />);
  const input = screen.getByPlaceholderText(/escribe un nombre/i); // CORREGIDO
  fireEvent.change(input, { target: { value: "zzz" } });
  expect(screen.getByText(/no encontrado/i)).toBeInTheDocument();
});
