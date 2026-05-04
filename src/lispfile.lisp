(defun cadr (lst) (car (cdr lst)))
(defun concatenate (&rest args) (+ args))
(defun length (lst)
    (if
        (null lst)
            0
            (length (cdr lst))
        )
    )
