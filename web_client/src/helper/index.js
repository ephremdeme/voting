import { useMediaQuery } from "react-responsive";

export const Desktop = ({ children }) => {
  const isDesktop = useMediaQuery({ minWidth: 992 });
  return isDesktop ? children : null;
};
export const Tablet = ({ children }) => {
  const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 991 });
  return isTablet ? children : null;
};

export const MobileOrTablet = ({ children }) => {
  const isMobileOrTablet = useMediaQuery({ maxWidth: 991 });
  return isMobileOrTablet ? children : null;
};

export const Mobile = ({ children }) => {
  const isMobile = useMediaQuery({ maxWidth: 767 });
  return isMobile ? children : null;
};
export const Default = ({ children }) => {
  const isNotMobile = useMediaQuery({ minWidth: 768 });
  return isNotMobile ? children : null;
};

var months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export const month = (id) => months[id];

export const getDate = (date) =>
  new Date(parseInt(date))
    .toGMTString()
    .replace("GMT", "")
    .replace(":00 ", "")
    .replace("00:00", "");

export const tokenConfig = () => {
  const token = localStorage.getItem("token");
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
    accept: "application/json",
  };
  if (token) config.headers["Authorization"] = `Bearer ${token}`;
  return config;
};
