(defun 1+ (var) (begin (+ var 1)))
(defun 1- (var) (begin (- var 1)))

(defmacro incr (var) `(set! ,var (1+ ,var)))
(defmacro decr (var) `(set! ,var (1- ,var)))

(setq indent 0)

(macroexpand-1 (incr indent))
(macroexpand-1 (decr indent))

(defun make-indentation (spc)
  (if (== spc 0) "" (+ (make-indentation (1- spc)) " ")))

(defmacro print-indent (&rest print-items)
  `(print (make-indentation indent) ,@print-items)
  )

(defun make-attr-assign (id-vals)
  (+ (if (> (length id-vals) 1)
         (+ " " (nth 0 id-vals) "=" (nth 1 id-vals)
            (make-attr-assign (cdr (cdr id-vals)))
            )
       
       " "))
    )


;(defmacro xml (key-attr &rest body)
;  `(let* ((data ',key-attr)
;         (key (if (list? data) (car data) data))
;         (attr (if (list? data) (cdr data) '()))
;         )
;     (print-indent (+ "<" key ,@(make-attr-assign attr) ">"))
;     (let* ((indent (+ indent 2))
;           )
;       ,@body
;       )
;     (print-indent (+ "</" key ">"))
;     )
;  )
                                        ;
(defmacro xml (key-attr &rest body)
  (let* ((is-list (list? key-attr))
         (tag (if is-list (car key-attr) key-attr))
         (attr-elements (if is-list (cdr key-attr) '())))
    `(let ((key ,tag)
           ;; Wir erstellen zur Laufzeit eine Liste aus den Attributen
           (attr (list ,@attr-elements))) 
       (print-indent (+ "<" key (make-attr-assign attr) ">"))
       (let ((indent (+ indent 2)))
         ,@body)
       (print-indent (+ "</" key ">")))))

(defun mache-zaehler (startwert)
  (let ((wert startwert)) ; Hier wird die Umgebung mit 'wert' erstellt
    (lambda (msg)
      (cond ((== msg 'hole-wert) wert)
            ((== msg 'incr) (set! wert (+ wert 1)) wert)
            ((== msg 'decr) (set! wert (- wert 1)) wert)
            ((== msg 'post-incr) (let ((old wert)) (set! wert (+ wert 1)) old))
            ((== msg 'post-decr) (let ((old wert)) (set! wert (- wert 1)) old))
            (else "Unbekannt")))))

(setq next-id (mache-zaehler 0))

(next-id 'hole-wert)
(next-id 'incr)
(next-id 'post-incr)
(next-id 'hole-wert)



(xml ("test" "id" (next-id 'post-incr))
     (xml ("level1" "id" (next-id 'post-incr))
          (xml "level2"
               (print-indent "text" )
               )
          )
     )

