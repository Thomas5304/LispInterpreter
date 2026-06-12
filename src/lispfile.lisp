
(defun 1+ (var) (begin (+ var 1)))
(defun 1- (var) (begin (- var 1)))

(defmacro incr (var &optional (diff 1)) `(begin (set! ,var (+ ,var ,diff)) ,var))
(defmacro decr (var &optional (diff 1)) `(begin (set! ,var (- ,var ,diff)) ,var))

(defun cadr (lst) (car (cdr lst)))
(defun nth (n lst) (if (<= n 0) (car lst) (nth (1- n) (cdr lst))))
(defun concatenate (&rest args) (+ args))
(defun length (lst)
    (if
        (null lst)
            0
            (+ (length (cdr lst)) 1)
        )
    )
;(defmacro my-and (&rest expr)
;    (begin
;    (print expr)
;    (cond
;        ((null expr) (print "emptylist") t)
;        ((null (cdr expr)) (print "one element") ,(car expr))
;        (else `(if ,(car expr) (my-and ,@(cdr expr)))
;        )
;    ))
;)
;(defmacro my-cond (&rest branches)
;    (if (null branches)
;        nil
;        (let (
;                (part-1 (car branches))
;                (last (cdr branches))
;                (condition (car part-1))
;                (body (cdr part-1))
;            )
;            `(if ,condition (begin ,@body)
;                (my-cond ,@last)
;
;            )
;        )
;    )
;)
(defmacro when (condition &rest body)
    `(if ,condition (begin ,@body ) nil)
)
(defmacro unless (condition &rest body)
    `(if (not ,condition) (begin ,@body) nil)
)
(defmacro for (var from start to end &rest body)
  `(let ((,var ,start)
	 (max ,end))
     (while (< ,var max)
       ,@body
       (define ,var (+ ,var 1))
       )
     )
  )
(defmacro progn (&rest body) `(begin ,@body))
(defun dont-quit () (set! __.QUIT.__ nil))

(defmacro swap (var1 var2) (let ((tmp (gensym )))
    `(let ((,tmp ,var1)) (set! ,var1 ,var2) (set! ,var2 ,tmp) (list ,var1 ,var2))
  ))


((defmacro mk-counter (name &key (start 0) (increment 1))
  (let ((pre-plus (intern (format "++{}" name)))    ;; Erzeugt z.B. zähler-1+
        (pre-minus (intern (format "--{}" name)))   ;; Erzeugt z.B. zähler-1-
        (post-plus (intern (format "{}++" name)))    ;; Erzeugt z.B. zähler-1+
        (post-minus (intern (format "{}--" name)))   ;; Erzeugt z.B. zähler-1-
        (get (intern (format "get-{}" name))) ;; Erzeugt z.B. get-zähler-1
        (values (intern (format "values-{}" name))))
    `(let ((counter ,start))
       (defun ,pre-plus () (begin (incr counter ,increment) counter))
       (defun ,pre-minus () (begin (decr counter ,increment) counter))
       (defun ,post-plus () (let ((old counter)) (incr counter ,increment) old))
       (defun ,post-minus () (let ((old counter)) (decr counter ,increment) old))
       ;(defun ,name () (list ',name "value" counter "start" ,start "increment" ,increment))
       (defun ,values () (list ',name counter ,start ,increment))
       (defun ,get () counter))))
