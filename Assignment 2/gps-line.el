(defun gps-line ()
  "Print the current buffer line number, narrowed line number of point, and total number of newline characters in the buffer."
  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos))
        (newline-count (count-matches "\n" (point-min) (point-max))))
    (if (= start 1)
        (message "Line %d/%d" n newline-count)
      (save-excursion
        (save-restriction
          (widen)
          (message "line %d (narrowed line %d)/%d"
                   (+ n (line-number-at-pos start) -1) n newline-count))))))
