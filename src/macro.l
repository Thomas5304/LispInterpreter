(defmacro unless (cond body) (quasiquote (if (not (unquote cond)) (unquote body))))
(unless t (print "Fail"))
(unless nil (print "Pass"))
