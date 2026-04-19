import { AuthStatusPanel } from "@/components/auth/auth-status-panel";
import { PageHeading } from "@/components/page-heading";

export default function SignUpPage() {
  return (
    <>
      <PageHeading
        description="Create an account before checkout so package access remains available after purchase."
        eyebrow="Auth"
        title="Sign up"
      />
      <div className="mx-auto max-w-xl px-6 py-8 sm:px-10 lg:px-14">
        <AuthStatusPanel mode="sign-up" />
      </div>
    </>
  );
}
