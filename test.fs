let x = 5

let fval x = x

let f x =
    fval x

let is_a_member name = true

let check_membership name =
    if is_a_member name then
        printfn "Welcome to the club"
    else
        printfn "You're not a member. Go away."
