local set = {}
for n in io.lines(arg[1]) do
    if not set[n] then
        print(n)
        set[n] = true
    end
end
