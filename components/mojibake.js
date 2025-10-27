"use client";
import { useState } from "react";

export default function useMojibake() {
  const [value, setValue] = useState("");
  const [isMojibake, setIsMojibake] = useState(false);

  // 文字化け関数（適当な不可読文字に変換）
  const toMojibake = (str) => {
    return str
      .split("")
      .map(() => String.fromCharCode(0x3000 + Math.floor(Math.random() * 2000)))
      .join("");
  };

  const handleChange = (e) => {
    const input = e.target.value;
    // 100文字を超えた瞬間にフラグを立てる
    if (!isMojibake && input.length > 100) {
      setIsMojibake(true);
    }
    setValue(input);
  };

  const displayValue = isMojibake ? toMojibake(value) : value;

  return { value: displayValue, handleChange };
}
