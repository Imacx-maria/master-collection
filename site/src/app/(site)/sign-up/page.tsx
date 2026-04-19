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
      <div className="mx-auto max-w-xl p-4 sm:p-6">
        <AuthStatusPanel mode="sign-up" />
      </div>
    </>
  );
}
