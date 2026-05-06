(defun cadr (lst) (car (cdr lst)))
(defun nth (n lst) (if (<= n 0) (car lst) (nth (- n 1) (cdr lst))))
(defun concatenate (&rest args) (+ args))
(defun length (lst)
    (if
        (null lst)
            0
            (+ (length (cdr lst)) 1)
        )
    )
