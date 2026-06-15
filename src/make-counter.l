(defun make-counter ()
  (let ((n 0))
    (lambda () (setq n (+ n 1)) n)
    )
  )

;(setq c (make-counter))
