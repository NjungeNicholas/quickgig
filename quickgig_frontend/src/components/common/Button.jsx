const Button = ({ children, onClick, variant }) => {
    const buttonStyles = variant === 'primary'
        ? "bg-primary text-white py-2 px-4 rounded hover:bg-secondary"
        : "bg-secondary text-white py-2 px-4 rounded hover:bg-primary";
    return (
        <button className={`font-body ${buttonStyles}`} onClick={onClick}>
            {children}
        </button>
    );
};

export default Button;
